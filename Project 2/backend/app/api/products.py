from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from backend.app.schemas.all_schemas import ProductResponse, ProductListResponse, CategoryResponse
from backend.app.core.supabase_client import get_supabase_client
from backend.app.core.datastore import store

router = APIRouter(tags=["Products & Categories"])

@router.get("/categories", response_model=List[CategoryResponse])
async def list_categories():
    """Retrieve all product categories."""
    supabase = get_supabase_client()
    if supabase:
        try:
            res = supabase.table("categories").select("*").order("name").execute()
            if res.data:
                return res.data
        except Exception:
            pass

    return store.get_data().get("categories", [])

@router.get("/products", response_model=ProductListResponse)
async def list_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = Query("newest", pattern="^(newest|price_asc|price_desc|popularity)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50)
):
    """Retrieve products with filtering, search, pricing ranges, and sorting."""
    # Read product dataset
    supabase = get_supabase_client()
    raw_products = []
    categories = {c["id"]: c["name"] for c in store.get_data().get("categories", [])}

    if supabase:
        try:
            query = supabase.table("products").select("*, categories(name)").eq("is_active", True)
            if min_price is not None:
                query = query.gte("price", min_price)
            if max_price is not None:
                query = query.lte("price", max_price)
            if search:
                query = query.ilike("name", f"%{search}%")

            res = query.execute()
            if res.data:
                for p in res.data:
                    cat_name = p.get("categories", {}).get("name") if isinstance(p.get("categories"), dict) else None
                    raw_products.append({**p, "category_name": cat_name})
        except Exception:
            raw_products = []

    if not raw_products:
        # Fallback to local high-fidelity data store
        all_p = [p for p in store.get_data().get("products", []) if p.get("is_active", True)]
        for p in all_p:
            p_cat = categories.get(p.get("category_id"), "")
            raw_products.append({**p, "category_name": p_cat})

        # Apply category filter
        if category and category != "all":
            # Can match category id or category slug
            cat_list = store.get_data().get("categories", [])
            target_cat_id = None
            for c in cat_list:
                if c["slug"] == category or c["id"] == category:
                    target_cat_id = c["id"]
                    break
            if target_cat_id:
                raw_products = [p for p in raw_products if p.get("category_id") == target_cat_id]

        # Apply search filter
        if search:
            s_lower = search.lower().strip()
            raw_products = [
                p for p in raw_products 
                if s_lower in p["name"].lower() or s_lower in p.get("description", "").lower()
            ]

        # Apply price filters
        if min_price is not None:
            raw_products = [p for p in raw_products if float(p["price"]) >= min_price]
        if max_price is not None:
            raw_products = [p for p in raw_products if float(p["price"]) <= max_price]

    # Sort
    if sort_by == "price_asc":
        raw_products.sort(key=lambda x: float(x["price"]))
    elif sort_by == "price_desc":
        raw_products.sort(key=lambda x: float(x["price"]), reverse=True)
    elif sort_by == "popularity":
        raw_products.sort(key=lambda x: x.get("stock_quantity", 0))
    else:  # newest
        raw_products.sort(key=lambda x: str(x.get("created_at", "")), reverse=True)

    total = len(raw_products)
    total_pages = max(1, (total + page_size - 1) // page_size)
    offset = (page - 1) * page_size
    items = raw_products[offset:offset + page_size]

    return ProductListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product_details(product_id: str):
    """Retrieve full product details by id or slug."""
    supabase = get_supabase_client()
    categories = {c["id"]: c["name"] for c in store.get_data().get("categories", [])}

    if supabase:
        try:
            res = supabase.table("products").select("*, categories(name)").or_(f"id.eq.{product_id},slug.eq.{product_id}").execute()
            if res.data and len(res.data) > 0:
                p = res.data[0]
                cat_name = p.get("categories", {}).get("name") if isinstance(p.get("categories"), dict) else None
                return {**p, "category_name": cat_name}
        except Exception:
            pass

    # Fallback to local store
    for p in store.get_data().get("products", []):
        if p["id"] == product_id or p["slug"] == product_id:
            p_cat = categories.get(p.get("category_id"), "")
            return {**p, "category_name": p_cat}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
