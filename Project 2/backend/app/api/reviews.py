import uuid
from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.schemas.all_schemas import ReviewCreate, ReviewResponse
from backend.app.dependencies.auth import get_current_user, AuthenticatedUser
from backend.app.core.datastore import store

router = APIRouter(prefix="/products", tags=["Product Reviews"])

@router.get("/{product_id}/reviews", response_model=List[ReviewResponse])
async def get_product_reviews(product_id: str):
    """Retrieve reviews for a given product."""
    data = store.get_data()
    reviews = [r for r in data.get("reviews", []) if r["product_id"] == product_id]
    return reviews

@router.post("/{product_id}/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_product_review(
    product_id: str,
    review_in: ReviewCreate,
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Add a verified review for a product."""
    data = store.get_data()
    products = data.get("products", [])
    if not any(p["id"] == product_id for p in products):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    reviews = data.setdefault("reviews", [])
    # Check if user already reviewed
    for r in reviews:
        if r["product_id"] == product_id and r["user_id"] == user.id:
            # Update existing review
            r["rating"] = review_in.rating
            r["review_text"] = review_in.review_text
            r["created_at"] = datetime.now(timezone.utc).isoformat()
            store.save()
            return ReviewResponse(**r)

    new_review = {
        "id": f"rev-{uuid.uuid4().hex[:12]}",
        "user_id": user.id,
        "user_name": user.full_name or "Verified Customer",
        "product_id": product_id,
        "rating": review_in.rating,
        "review_text": review_in.review_text,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    reviews.insert(0, new_review)
    store.save()
    return ReviewResponse(**new_review)
