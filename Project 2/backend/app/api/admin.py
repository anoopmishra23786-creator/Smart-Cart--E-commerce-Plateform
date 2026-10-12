import uuid
from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.schemas.all_schemas import (
    ProductCreate, ProductUpdate, ProductResponse,
    OrderStatusUpdate, OrderResponse, OrderItemResponse,
    AdminDashboardStats
)
from backend.app.dependencies.auth import get_current_admin, AuthenticatedUser
from backend.app.core.datastore import store

router = APIRouter(prefix="/admin", tags=["Administrator Dashboard"])

@router.get("/dashboard", response_model=AdminDashboardStats)
async def get_dashboard_metrics(admin: AuthenticatedUser = Depends(get_current_admin)):
    """Summary metrics of revenue, orders, products, and inventory for administrative control."""
    data = store.get_data()
    orders = data.get("orders", [])
    products = data.get("products", [])
    categories = data.get("categories", [])

    total_revenue = round(sum(o.get("total_amount", 0.0) for o in orders if o.get("order_status") != "cancelled"), 2)
    total_orders = len(orders)
    total_products = len(products)
    low_stock = sum(1 for p in products if p.get("stock_quantity", 0) <= 10)

    recent_orders = []
    for o in orders[:5]:
        items = [
            OrderItemResponse(**it) for it in data.get("order_items", [])
            if it["order_id"] == o["id"]
        ]
        recent_orders.append(OrderResponse(**o, items=items))

    # Top category count distribution
    cat_counts = []
    for c in categories:
        cnt = sum(1 for p in products if p.get("category_id") == c["id"])
        cat_counts.append({"name": c["name"], "count": cnt, "slug": c["slug"]})

    return AdminDashboardStats(
        total_revenue=total_revenue,
        total_orders=total_orders,
        total_products=total_products,
        low_stock_products=low_stock,
        recent_orders=recent_orders,
        top_categories=cat_counts
    )

@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product_in: ProductCreate, admin: AuthenticatedUser = Depends(get_current_admin)):
    """Admin-only: Create a new product."""
    data = store.get_data()
    products = data.setdefault("products", [])

    # Check slug collision
    if any(p["slug"] == product_in.slug for p in products):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A product with this slug already exists.")

    new_product = {
        "id": f"p-{uuid.uuid4().hex[:12]}",
        **product_in.model_dump(),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    products.insert(0, new_product)
    store.save()
    return ProductResponse(**new_product)

@router.patch("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product_in: ProductUpdate,
    admin: AuthenticatedUser = Depends(get_current_admin)
):
    """Admin-only: Update product information or adjust stock."""
    data = store.get_data()
    products = data.get("products", [])

    target = None
    for p in products:
        if p["id"] == product_id:
            target = p
            break

    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    update_dict = product_in.model_dump(exclude_unset=True)
    target.update(update_dict)
    target["updated_at"] = datetime.now(timezone.utc).isoformat()
    store.save()
    return ProductResponse(**target)

@router.delete("/products/{product_id}")
async def delete_product(product_id: str, admin: AuthenticatedUser = Depends(get_current_admin)):
    """Admin-only: Deactivate or delete product."""
    data = store.get_data()
    products = data.get("products", [])

    for p in products:
        if p["id"] == product_id:
            # Soft delete for order history integrity
            p["is_active"] = False
            p["updated_at"] = datetime.now(timezone.utc).isoformat()
            store.save()
            return {"status": "success", "message": f"Product '{p['name']}' has been deactivated."}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

@router.get("/orders", response_model=List[OrderResponse])
async def list_all_orders(admin: AuthenticatedUser = Depends(get_current_admin)):
    """Admin-only: Retrieve all system orders."""
    data = store.get_data()
    orders = data.get("orders", [])
    results = []
    for o in orders:
        items = [
            OrderItemResponse(**it) for it in data.get("order_items", [])
            if it["order_id"] == o["id"]
        ]
        results.append(OrderResponse(**o, items=items))
    return results

@router.patch("/orders/{order_id}", response_model=OrderResponse)
async def update_order_status(
    order_id: str,
    status_in: OrderStatusUpdate,
    admin: AuthenticatedUser = Depends(get_current_admin)
):
    """Admin-only: Update fulfillment or payment status of an order."""
    data = store.get_data()
    for o in data.get("orders", []):
        if o["id"] == order_id:
            o["order_status"] = status_in.order_status
            if status_in.payment_status:
                o["payment_status"] = status_in.payment_status
            store.save()
            items = [
                OrderItemResponse(**it) for it in data.get("order_items", [])
                if it["order_id"] == o["id"]
            ]
            return OrderResponse(**o, items=items)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
