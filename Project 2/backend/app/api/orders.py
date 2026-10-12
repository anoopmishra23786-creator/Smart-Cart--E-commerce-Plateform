import uuid
from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.schemas.all_schemas import (
    OrderCreate, OrderResponse, OrderItemResponse
)
from backend.app.dependencies.auth import get_current_user, AuthenticatedUser
from backend.app.core.config import settings
from backend.app.core.datastore import store

router = APIRouter(prefix="/orders", tags=["Orders & Checkout"])

def _find_product(product_id: str):
    for p in store.get_data().get("products", []):
        if p["id"] == product_id and p.get("is_active", True):
            return p
    return None

@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order_in: OrderCreate, user: AuthenticatedUser = Depends(get_current_user)):
    """
    Creates an order from current cart items.
    Enforces server-side price calculation, inventory decrement, and validation.
    """
    data = store.get_data()
    cart_items = [c for c in data.get("cart_items", []) if c["user_id"] == user.id]

    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot place order with an empty cart."
        )

    # Validate stock and calculate authoritative prices
    order_id = f"ord-{uuid.uuid4().hex[:12]}"
    created_items: List[OrderItemResponse] = []
    subtotal = 0.0

    # Verification phase
    for item in cart_items:
        prod = _find_product(item["product_id"])
        if not prod:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product with ID {item['product_id']} is no longer active."
            )
        if prod["stock_quantity"] < item["quantity"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient inventory for '{prod['name']}'. Only {prod['stock_quantity']} units remaining."
            )

    # Execution phase: decrement stock & construct line items
    for item in cart_items:
        prod = _find_product(item["product_id"])
        qty = item["quantity"]
        unit_price = float(prod["price"])
        line_total = round(unit_price * qty, 2)
        subtotal += line_total

        # Decrement stock safely
        prod["stock_quantity"] -= qty

        item_entry = {
            "id": f"item-{uuid.uuid4().hex[:12]}",
            "order_id": order_id,
            "product_id": prod["id"],
            "product_name": prod["name"],
            "unit_price": unit_price,
            "quantity": qty,
            "line_total": line_total
        }
        data.setdefault("order_items", []).append(item_entry)
        created_items.append(OrderItemResponse(**item_entry))

    subtotal = round(subtotal, 2)
    shipping_fee = 0.0 if subtotal >= settings.FREE_SHIPPING_THRESHOLD else settings.DEFAULT_SHIPPING_FEE
    total_amount = round(subtotal + shipping_fee, 2)

    addr = order_in.address
    formatted_address = f"{addr.address_line}, {addr.city}, {addr.state} - {addr.postal_code}, {addr.country}"

    order_record = {
        "id": order_id,
        "user_id": user.id,
        "recipient_name": addr.recipient_name,
        "phone": addr.phone,
        "shipping_address": formatted_address,
        "subtotal": subtotal,
        "shipping_fee": shipping_fee,
        "total_amount": total_amount,
        "order_status": "processing",
        "payment_method": order_in.payment_method,
        "payment_status": "paid" if order_in.payment_method != "cod" else "unpaid",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    data.setdefault("orders", []).insert(0, order_record)

    # Clear user's cart
    data["cart_items"] = [c for c in data.get("cart_items", []) if c["user_id"] != user.id]

    store.save()

    return OrderResponse(**order_record, items=created_items)

@router.get("", response_model=List[OrderResponse])
async def list_orders(user: AuthenticatedUser = Depends(get_current_user)):
    """Retrieve all orders belonging to the authenticated user."""
    data = store.get_data()
    user_orders = [o for o in data.get("orders", []) if o["user_id"] == user.id]

    results = []
    for o in user_orders:
        items = [
            OrderItemResponse(**it) for it in data.get("order_items", [])
            if it["order_id"] == o["id"]
        ]
        results.append(OrderResponse(**o, items=items))

    return results

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order_by_id(order_id: str, user: AuthenticatedUser = Depends(get_current_user)):
    """Retrieve a single order ensuring ownership or admin privilege."""
    data = store.get_data()
    for o in data.get("orders", []):
        if o["id"] == order_id:
            if o["user_id"] != user.id and not user.is_admin:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to this order.")
            
            items = [
                OrderItemResponse(**it) for it in data.get("order_items", [])
                if it["order_id"] == o["id"]
            ]
            return OrderResponse(**o, items=items)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
