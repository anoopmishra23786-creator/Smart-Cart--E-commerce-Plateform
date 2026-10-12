import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.schemas.all_schemas import (
    CartItemAdd, CartItemUpdate, CartItemResponse, CartSummaryResponse
)
from backend.app.dependencies.auth import get_current_user, AuthenticatedUser
from backend.app.core.config import settings
from backend.app.core.datastore import store
from backend.app.core.supabase_client import get_supabase_client

router = APIRouter(prefix="/cart", tags=["Shopping Cart"])

def _find_product(product_id: str):
    for p in store.get_data().get("products", []):
        if p["id"] == product_id and p.get("is_active", True):
            return p
    return None

@router.get("", response_model=CartSummaryResponse)
async def get_cart(user: AuthenticatedUser = Depends(get_current_user)):
    """Retrieve user cart with server-side recalculated prices and accurate totals."""
    items_response: List[CartItemResponse] = []
    subtotal = 0.0

    # Read from store for user
    cart_items = [c for c in store.get_data().get("cart_items", []) if c["user_id"] == user.id]

    for item in cart_items:
        product = _find_product(item["product_id"])
        if not product:
            continue
        
        # Server-enforced pricing: NEVER trust client price!
        unit_price = float(product["price"])
        qty = item["quantity"]
        # Stock safety check
        if qty > product["stock_quantity"]:
            qty = max(1, product["stock_quantity"])
            item["quantity"] = qty

        line_total = round(unit_price * qty, 2)
        subtotal += line_total

        items_response.append(CartItemResponse(
            id=item["id"],
            product_id=product["id"],
            product_name=product["name"],
            price=unit_price,
            image_url=product["image_url"],
            stock_quantity=product["stock_quantity"],
            quantity=qty,
            line_total=line_total
        ))

    subtotal = round(subtotal, 2)
    free_shipping = subtotal >= settings.FREE_SHIPPING_THRESHOLD or subtotal == 0
    shipping_fee = 0.0 if free_shipping else settings.DEFAULT_SHIPPING_FEE
    total = round(subtotal + shipping_fee, 2)

    return CartSummaryResponse(
        items=items_response,
        subtotal=subtotal,
        shipping_fee=shipping_fee,
        total=total,
        free_shipping_threshold=settings.FREE_SHIPPING_THRESHOLD,
        free_shipping_achieved=free_shipping
    )

@router.post("/items", response_model=CartSummaryResponse)
async def add_to_cart(item_in: CartItemAdd, user: AuthenticatedUser = Depends(get_current_user)):
    """Add a product or increment quantity in the cart."""
    product = _find_product(item_in.product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or inactive")

    if product["stock_quantity"] < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product is currently out of stock")

    data = store.get_data()
    cart_items = data.setdefault("cart_items", [])

    existing = None
    for c in cart_items:
        if c["user_id"] == user.id and c["product_id"] == item_in.product_id:
            existing = c
            break

    if existing:
        new_qty = existing["quantity"] + item_in.quantity
        if new_qty > product["stock_quantity"]:
            new_qty = product["stock_quantity"]
        existing["quantity"] = new_qty
    else:
        req_qty = min(item_in.quantity, product["stock_quantity"])
        cart_items.append({
            "id": f"cart-{uuid.uuid4().hex[:12]}",
            "user_id": user.id,
            "product_id": item_in.product_id,
            "quantity": req_qty
        })

    store.save()
    return await get_cart(user=user)

@router.patch("/items/{item_id}", response_model=CartSummaryResponse)
async def update_cart_item(item_id: str, update_in: CartItemUpdate, user: AuthenticatedUser = Depends(get_current_user)):
    """Update quantity of an item in the cart."""
    data = store.get_data()
    cart_items = data.get("cart_items", [])
    
    target = None
    for c in cart_items:
        if c["id"] == item_id and c["user_id"] == user.id:
            target = c
            break

    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

    product = _find_product(target["product_id"])
    if not product:
        cart_items.remove(target)
        store.save()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product no longer available")

    if update_in.quantity > product["stock_quantity"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only {product['stock_quantity']} units available in stock"
        )

    target["quantity"] = update_in.quantity
    store.save()
    return await get_cart(user=user)

@router.delete("/items/{item_id}", response_model=CartSummaryResponse)
async def remove_cart_item(item_id: str, user: AuthenticatedUser = Depends(get_current_user)):
    """Remove item from user's shopping cart."""
    data = store.get_data()
    cart_items = data.get("cart_items", [])

    initial_len = len(cart_items)
    data["cart_items"] = [c for c in cart_items if not (c["id"] == item_id and c["user_id"] == user.id)]

    if len(data["cart_items"]) == initial_len:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

    store.save()
    return await get_cart(user=user)
