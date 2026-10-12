import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.schemas.all_schemas import WishlistAdd, WishlistItemResponse
from backend.app.dependencies.auth import get_current_user, AuthenticatedUser
from backend.app.core.datastore import store

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])

def _find_product(product_id: str):
    for p in store.get_data().get("products", []):
        if p["id"] == product_id and p.get("is_active", True):
            return p
    return None

@router.get("", response_model=List[WishlistItemResponse])
async def get_wishlist(user: AuthenticatedUser = Depends(get_current_user)):
    """Retrieve all items in the user's wishlist."""
    items = []
    wishlists = [w for w in store.get_data().get("wishlists", []) if w["user_id"] == user.id]

    for w in wishlists:
        product = _find_product(w["product_id"])
        if product:
            items.append(WishlistItemResponse(
                id=w["id"],
                product_id=product["id"],
                product_name=product["name"],
                price=float(product["price"]),
                compare_at_price=float(product["compare_at_price"]) if product.get("compare_at_price") else None,
                image_url=product["image_url"],
                stock_quantity=product["stock_quantity"],
                created_at=w.get("created_at")
            ))
    return items

@router.post("/items", response_model=List[WishlistItemResponse])
async def add_to_wishlist(item_in: WishlistAdd, user: AuthenticatedUser = Depends(get_current_user)):
    """Add a product to user's wishlist."""
    product = _find_product(item_in.product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    data = store.get_data()
    wishlists = data.setdefault("wishlists", [])

    for w in wishlists:
        if w["user_id"] == user.id and w["product_id"] == item_in.product_id:
            return await get_wishlist(user=user)

    wishlists.append({
        "id": f"wish-{uuid.uuid4().hex[:12]}",
        "user_id": user.id,
        "product_id": item_in.product_id
    })
    store.save()
    return await get_wishlist(user=user)

@router.delete("/items/{item_id}", response_model=List[WishlistItemResponse])
async def remove_from_wishlist(item_id: str, user: AuthenticatedUser = Depends(get_current_user)):
    """Remove an item from wishlist (matches item id or product id)."""
    data = store.get_data()
    wishlists = data.get("wishlists", [])

    data["wishlists"] = [
        w for w in wishlists
        if not (w["user_id"] == user.id and (w["id"] == item_id or w["product_id"] == item_id))
    ]
    store.save()
    return await get_wishlist(user=user)
