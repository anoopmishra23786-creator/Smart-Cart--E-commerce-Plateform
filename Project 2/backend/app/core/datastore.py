import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid

# Path to mock storage json for offline/local resilience
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
MOCK_FILE = os.path.join(DATA_DIR, "store_db.json")

def _init_mock_data() -> Dict[str, Any]:
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(MOCK_FILE):
        try:
            with open(MOCK_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    default_data: Dict[str, Any] = {
        "categories": [
            {
                "id": "c1000000-0000-0000-0000-000000000001",
                "name": "Electronics & Gadgets",
                "slug": "electronics",
                "description": "High-performance smart audio, wearables, and productivity accessories.",
                "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80"
            },
            {
                "id": "c1000000-0000-0000-0000-000000000002",
                "name": "Men & Women Fashion",
                "slug": "fashion",
                "description": "Contemporary streetwear, premium linen shirts, and minimalist apparel.",
                "image_url": "https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=800&auto=format&fit=crop&q=80"
            },
            {
                "id": "c1000000-0000-0000-0000-000000000003",
                "name": "Home & Kitchen Essentials",
                "slug": "home-essentials",
                "description": "Artisan ceramic tableware, ergonomic workstations, and indoor lifestyle decor.",
                "image_url": "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?w=800&auto=format&fit=crop&q=80"
            },
            {
                "id": "c1000000-0000-0000-0000-000000000004",
                "name": "Watches & Accessories",
                "slug": "accessories",
                "description": "Handcrafted leather goods, precision chronograph timepieces, and travel gear.",
                "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80"
            }
        ],
        "products": [
            {
                "id": "p1000000-0000-0000-0000-000000000001",
                "category_id": "c1000000-0000-0000-0000-000000000001",
                "name": "AuraWave Pro ANC Wireless Headphones",
                "slug": "aurawave-pro-anc-headphones",
                "description": "Studio-grade acoustic architecture with adaptive hybrid active noise cancellation, 40-hour continuous playback, and ultra-plush memory foam earcups.",
                "price": 4999.00,
                "compare_at_price": 7499.00,
                "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80",
                "stock_quantity": 45,
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": "p1000000-0000-0000-0000-000000000002",
                "category_id": "c1000000-0000-0000-0000-000000000001",
                "name": "PulseFit Horizon GPS Smartwatch",
                "slug": "pulsefit-horizon-smartwatch",
                "description": "Aerospace-grade zinc alloy casing featuring a 1.43-inch AMOLED sunlight display, continuous SpO2 biometric monitoring, 5ATM water resistance, and built-in dual-band GPS.",
                "price": 3299.00,
                "compare_at_price": 4999.00,
                "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80",
                "stock_quantity": 30,
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": "p1000000-0000-0000-0000-000000000003",
                "category_id": "c1000000-0000-0000-0000-000000000001",
                "name": "HyperKey Wireless Mechanical Keyboard",
                "slug": "hyperkey-wireless-mechanical-keyboard",
                "description": "Compact 75% hot-swappable mechanical keyboard equipped with factory-lubed linear switches, sound-dampening silicone gasket mount, and tri-mode Bluetooth 5.2/2.4G connectivity.",
                "price": 3799.00,
                "compare_at_price": 5299.00,
                "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&auto=format&fit=crop&q=80",
                "stock_quantity": 25,
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": "p1000000-0000-0000-0000-000000000004",
                "category_id": "c1000000-0000-0000-0000-000000000001",
                "name": "OmniGlide Ergonomic Precision Mouse",
                "slug": "omniglide-ergonomic-mouse",
                "description": "Sculpted 57-degree vertical grip engineered to alleviate wrist strain. Features silent magnetic scroll wheel, multi-device flow switching, and 4000 DPI darkfield sensor.",
                "price": 1899.00,
                "compare_at_price": 2499.00,
                "image_url": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800&auto=format&fit=crop&q=80",
                "stock_quantity": 50,
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": "p1000000-0000-0000-0000-000000000005",
                "category_id": "c1000000-0000-0000-0000-000000000002",
                "name": "Bespoke Pure French Linen Casual Shirt",
                "slug": "bespoke-pure-linen-shirt",
                "description": "Spun from 100% Normandy flax fiber. Naturally breathable, pre-washed for vintage softness, featuring mother-of-pearl buttons and relaxed modern tailoring.",
                "price": 2199.00,
                "compare_at_price": 3199.00,
                "image_url": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=800&auto=format&fit=crop&q=80",
                "stock_quantity": 40,
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": "p1000000-0000-0000-0000-000000000006",
                "category_id": "c1000000-0000-0000-0000-000000000002",
                "name": "UrbanKnit Heavyweight Cotton Hoodie",
                "slug": "urbanknit-heavyweight-hoodie",
                "description": "450 GSM French terry combed cotton offering a structured drop-shoulder drape, double-layered hood, and reinforced ribbed hems.",
                "price": 2499.00,
                "compare_at_price": 3499.00,
                "image_url": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=800&auto=format&fit=crop&q=80",
                "stock_quantity": 35,
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": "p1000000-0000-0000-0000-000000000007",
                "category_id": "c1000000-0000-0000-0000-000000000002",
                "name": "Selvedge Tapered Indigo Denim Jeans",
                "slug": "selvedge-tapered-indigo-jeans",
                "description": "13.5 oz shuttle-loom woven Japanese selvedge denim. Clean dark-indigo rope dye that ages gracefully with custom whiskers and fades.",
                "price": 2999.00,
                "compare_at_price": 4299.00,
                "image_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=800&auto=format&fit=crop&q=80",
                "stock_quantity": 28,
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": "p1000000-0000-0000-0000-000000000008",
                "category_id": "c1000000-0000-0000-0000-000000000003",
                "name": "Nordic Matte Ceramic Pour-Over Set",
                "slug": "nordic-ceramic-pour-over-set",
                "description": "Handmade stoneware coffee dripper with spiral interior flow channels, wooden collar base, and 600ml borosilicate serving carafe.",
                "price": 1499.00,
                "compare_at_price": 1999.00,
                "image_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=800&auto=format&fit=crop&q=80",
                "stock_quantity": 20,
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": "p1000000-0000-0000-0000-000000000009",
                "category_id": "c1000000-0000-0000-0000-000000000003",
                "name": "AuraGlow Ambient Minimalist Desk Lamp",
                "slug": "auraglow-minimalist-desk-lamp",
                "description": "Sandblasted anodized aluminum housing with step-less touch dimming, 3 color temperatures (2700K-6500K), and USB-C power delivery.",
                "price": 1799.00,
                "compare_at_price": 2599.00,
                "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800&auto=format&fit=crop&q=80",
                "stock_quantity": 22,
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": "p1000000-0000-0000-0000-000000000010",
                "category_id": "c1000000-0000-0000-0000-000000000003",
                "name": "Botanica Ultrasonic Aromatherapy Diffuser",
                "slug": "botanica-ultrasonic-diffuser",
                "description": "Real bamboo wood exterior with 400ml water chamber, ultra-quiet whisper motor, automatic waterless shut-off, and subtle warm ambient illumination.",
                "price": 1299.00,
                "compare_at_price": 1899.00,
                "image_url": "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=800&auto=format&fit=crop&q=80",
                "stock_quantity": 30,
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": "p1000000-0000-0000-0000-000000000011",
                "category_id": "c1000000-0000-0000-0000-000000000004",
                "name": "Classic Heritage Chronograph Watch",
                "slug": "classic-heritage-chronograph-watch",
                "description": "Japanese precision quartz movement with domed sapphire crystal glass, 316L surgical stainless steel body, and genuine vegetable-tanned Italian leather band.",
                "price": 4499.00,
                "compare_at_price": 6499.00,
                "image_url": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=800&auto=format&fit=crop&q=80",
                "stock_quantity": 18,
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": "p1000000-0000-0000-0000-000000000012",
                "category_id": "c1000000-0000-0000-0000-000000000004",
                "name": "Artisan Full-Grain Leather Bi-Fold Wallet",
                "slug": "artisan-leather-bifold-wallet",
                "description": "Hand-stitched burnished saddle leather with RFID-blocking aluminum weave lining, 6 card slots, dual cash sleeve, and minimal profile.",
                "price": 1199.00,
                "compare_at_price": 1699.00,
                "image_url": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=800&auto=format&fit=crop&q=80",
                "stock_quantity": 60,
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
        ],
        "cart_items": [],
        "wishlists": [],
        "addresses": [],
        "orders": [],
        "order_items": [],
        "reviews": [
            {
                "id": "r1000000-0000-0000-0000-000000000001",
                "user_id": "u1000000-0000-0000-0000-000000000001",
                "user_name": "Aarav Sharma",
                "product_id": "p1000000-0000-0000-0000-000000000001",
                "rating": 5,
                "review_text": "Remarkable noise isolation during domestic flights. The battery easily lasted three whole working days on a single charge.",
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": "r1000000-0000-0000-0000-000000000002",
                "user_id": "u1000000-0000-0000-0000-000000000002",
                "user_name": "Priya Nair",
                "product_id": "p1000000-0000-0000-0000-000000000005",
                "rating": 5,
                "review_text": "The linen fabric texture is wonderfully breathable in warm humid weather. Precise stitching and fit.",
                "created_at": datetime.now(timezone.utc).isoformat()
            }
        ],
        "profiles": [
            {
                "id": "demo-admin-id",
                "email": "admin@smartcart.local",
                "full_name": "SmartCart Administrator",
                "phone": "+91 98765 43210",
                "is_admin": True,
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": "demo-user-id",
                "email": "customer@smartcart.local",
                "full_name": "Rahul Verma",
                "phone": "+91 98765 12345",
                "is_admin": False,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
        ]
    }
    with open(MOCK_FILE, "w", encoding="utf-8") as f:
        json.dump(default_data, f, indent=2)
    return default_data

class DataStore:
    def __init__(self):
        self._data = _init_mock_data()

    def get_data(self) -> Dict[str, Any]:
        return self._data

    def save(self):
        with open(MOCK_FILE, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)

store = DataStore()
