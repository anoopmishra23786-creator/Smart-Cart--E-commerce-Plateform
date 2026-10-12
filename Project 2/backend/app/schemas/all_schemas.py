from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

# --- Category Schemas ---
class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    image_url: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: str
    created_at: Optional[datetime] = None

# --- Product Schemas ---
class ProductBase(BaseModel):
    category_id: str
    name: str
    slug: str
    description: str
    price: float = Field(..., ge=0)
    compare_at_price: Optional[float] = Field(None, ge=0)
    image_url: str
    stock_quantity: int = Field(0, ge=0)
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    category_id: Optional[str] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    compare_at_price: Optional[float] = Field(None, ge=0)
    image_url: Optional[str] = None
    stock_quantity: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None

class ProductResponse(ProductBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    category_name: Optional[str] = None

class ProductListResponse(BaseModel):
    items: List[ProductResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

# --- Cart Schemas ---
class CartItemAdd(BaseModel):
    product_id: str
    quantity: int = Field(1, ge=1)

class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=1)

class CartItemResponse(BaseModel):
    id: str
    product_id: str
    product_name: str
    price: float
    image_url: str
    stock_quantity: int
    quantity: int
    line_total: float

class CartSummaryResponse(BaseModel):
    items: List[CartItemResponse]
    subtotal: float
    shipping_fee: float
    total: float
    free_shipping_threshold: float
    free_shipping_achieved: bool

# --- Wishlist Schemas ---
class WishlistAdd(BaseModel):
    product_id: str

class WishlistItemResponse(BaseModel):
    id: str
    product_id: str
    product_name: str
    price: float
    compare_at_price: Optional[float] = None
    image_url: str
    stock_quantity: int
    created_at: Optional[datetime] = None

# --- Order Schemas ---
class OrderAddress(BaseModel):
    recipient_name: str
    phone: str
    address_line: str
    city: str
    state: str
    postal_code: str
    country: str = "India"

class OrderCreate(BaseModel):
    address: OrderAddress
    payment_method: str = Field("cod", pattern="^(cod|card_demo|upi_demo|netbanking_demo)$")

class OrderItemResponse(BaseModel):
    id: str
    product_id: str
    product_name: str
    unit_price: float
    quantity: int
    line_total: float

class OrderResponse(BaseModel):
    id: str
    user_id: str
    recipient_name: str
    phone: str
    shipping_address: str
    subtotal: float
    shipping_fee: float
    total_amount: float
    order_status: str
    payment_method: str
    payment_status: str
    created_at: Optional[datetime] = None
    items: List[OrderItemResponse] = []

class OrderStatusUpdate(BaseModel):
    order_status: str = Field(..., pattern="^(pending|processing|shipped|delivered|cancelled)$")
    payment_status: Optional[str] = Field(None, pattern="^(unpaid|paid|refunded)$")

# --- Review Schemas ---
class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    review_text: str = Field(..., min_length=3, max_length=1000)

class ReviewResponse(BaseModel):
    id: str
    user_id: str
    user_name: Optional[str] = "Verified Customer"
    product_id: str
    rating: int
    review_text: str
    created_at: Optional[datetime] = None

# --- User & Profile Schemas ---
class UserProfile(BaseModel):
    id: str
    email: Optional[str] = None
    full_name: str
    phone: Optional[str] = None
    is_admin: bool = False
    created_at: Optional[datetime] = None

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None

# --- Admin Dashboard Stats ---
class AdminDashboardStats(BaseModel):
    total_revenue: float
    total_orders: int
    total_products: int
    low_stock_products: int
    recent_orders: List[OrderResponse] = []
    top_categories: List[Dict[str, Any]] = []
