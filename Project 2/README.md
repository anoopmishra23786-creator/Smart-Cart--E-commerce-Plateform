# SmartCart - Modern E-Commerce Platform

A production-grade, human-crafted full-stack e-commerce web platform built with **FastAPI (Python 3.11+)**, **Supabase (PostgreSQL & Authentication)**, **Bootstrap 5**, and **Vanilla JavaScript**.

SmartCart emphasizes real functionality, clean modular architecture, server-side price recalculation, stock concurrency control, and authentic usability rather than generic AI templates.

---

## 🌟 Key Features

1. **Storefront & Catalog**
   - Categorized catalog (Electronics, Fashion, Home Essentials, Accessories) priced accurately in INR (₹).
   - Real-time keyword search, category filters, and price ranges.
   - Server-side sorting by newest arrivals, price ascending/descending, and popularity.
   - Detailed product view with stock checks, specifications, customer reviews, and ratings.

2. **Shopping Cart & Checkout**
   - Stock-checked, persistent user shopping cart.
   - **Zero Client Trust:** All subtotals and totals are recalculated server-side; client prices are completely disregarded.
   - Dynamic free-delivery threshold (free express shipping on orders &ge; ₹999).
   - Structured shipping address capture with PIN code validation.
   - Simulated checkout modes (Cash on Delivery, UPI Instant Demo, Sandbox Card).

3. **Authentication & Security**
   - Supabase Auth session support and cryptographic JWT signature validation.
   - Strict server-side Role-Based Access Control (RBAC).
   - Supabase Row Level Security (RLS) policies safeguarding profiles, cart items, wishlists, and orders.

4. **User & Admin Dashboards**
   - Customer profile dashboard with order history and tracking.
   - Personal wishlist with "Move to Cart" workflows.
   - Dedicated Admin Console (`/admin/index.html`) with live PostgreSQL sales revenue metrics, product inventory editing, and order fulfillment status updates.

5. **API & Developer Experience**
   - Interactive Swagger API documentation at `/docs` and ReDoc at `/redoc`.
   - Comprehensive automated test suite (`pytest`) verifying health, inventory, authentication, and RBAC.

---

## 🏗️ Architecture & Technology Stack

```
Project 2/
├── backend/
│   └── app/
│       ├── api/               # Modular REST API routes
│       │   ├── auth.py        # /api/auth/me profile retrieval
│       │   ├── products.py    # /api/products & /api/categories
│       │   ├── cart.py        # /api/cart & cart management
│       │   ├── wishlist.py    # /api/wishlist
│       │   ├── orders.py      # /api/orders (creation & tracking)
│       │   ├── reviews.py     # /api/products/{id}/reviews
│       │   └── admin.py       # /api/admin metrics, catalog, and orders
│       ├── core/
│       │   ├── config.py      # Pydantic BaseSettings environment config
│       │   ├── supabase_client.py # Client factory
│       │   └── datastore.py   # High-fidelity storage engine & fallback
│       ├── dependencies/
│       │   └── auth.py        # JWT verification & role authorization dependencies
│       ├── schemas/
│       │   └── all_schemas.py # Pydantic v2 validation models
│       └── main.py            # FastAPI ASGI entrypoint & static mount
├── frontend/
│   ├── index.html             # Homepage with best sellers & hero
│   ├── shop.html              # Search, filterable catalog & pagination
│   ├── product.html           # Product details, stock & customer reviews
│   ├── cart.html              # Dynamic cart management
│   ├── checkout.html          # Order address & simulated payment
│   ├── login.html             # Supabase & demo credential login
│   ├── register.html          # Customer registration
│   ├── account.html           # User profile center
│   ├── orders.html            # Order tracking & invoice history
│   ├── wishlist.html          # Saved wishlist
│   ├── admin/
│   │   └── index.html         # Admin dashboard & inventory control
│   └── assets/
│       ├── css/style.css      # Refined design system tokens & styles
│       └── js/
│           ├── api.js         # Centralized Fetch API client
│           └── app.js         # Navbar state, toasts, formatters
├── supabase/
│   ├── schema.sql             # Complete PostgreSQL schema & RLS policies
│   └── seed.sql               # Realistic catalog seed data
├── tests/
│   └── test_api.py            # Automated pytest suite
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## 🚀 Quickstart & Local Setup (Windows)

### 1. Prerequisites
- Python 3.11+
- Git

### 2. Environment Setup
Clone the repository and navigate into the project directory:
```powershell
git clone <your-repo-url>
cd "Project 2"
```

Create and activate a virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:
```powershell
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy `.env.example` to `.env`:
```powershell
copy .env.example .env
```

*(Optional)* If you have an active Supabase project:
1. Open your Supabase Dashboard -> **SQL Editor**.
2. Run `supabase/schema.sql` to initialize tables, constraints, and RLS policies.
3. Run `supabase/seed.sql` to populate initial demo products.
4. Copy `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, and `SUPABASE_JWT_SECRET` into `.env`.

*Note: SmartCart includes an automatic fallback data engine so you can run, test, and present the full end-to-end platform immediately out of the box even before configuring cloud database credentials.*

### 4. Start the Application
Run the FastAPI ASGI server:
```powershell
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 5. Access the Web Application
- **Storefront:** [http://127.0.0.1:8000/index.html](http://127.0.0.1:8000/index.html)
- **Product Catalog:** [http://127.0.0.1:8000/shop.html](http://127.0.0.1:8000/shop.html)
- **Interactive API Docs (Swagger):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Admin Console:** [http://127.0.0.1:8000/admin/index.html](http://127.0.0.1:8000/admin/index.html)
  *(Quick access: On `/login.html`, click **Admin Demo**)*

---

## 🧪 Running Automated Tests

Run the backend test suite:
```powershell
python -m pytest tests/test_api.py -v
```

Expected output:
```
tests/test_api.py::test_api_health PASSED
tests/test_api.py::test_list_products_and_pagination PASSED
tests/test_api.py::test_product_detail_and_not_found PASSED
tests/test_api.py::test_categories_listing PASSED
tests/test_api.py::test_unauthenticated_cart_access PASSED
tests/test_api.py::test_customer_cart_and_server_price_validation PASSED
tests/test_api.py::test_admin_authorization_enforcement PASSED
tests/test_api.py::test_invalid_token_handling PASSED
======================== 8 passed in 3.51s =========================
```

---

## 🔒 Supabase Security & Row Level Security (RLS)

All user-facing tables enforce PostgreSQL RLS policies in `supabase/schema.sql`:
- **Profiles**: Public read for author info; updates restricted strictly to `auth.uid() = id`.
- **Products & Categories**: Public read only for `is_active = TRUE`. Creation and modifications restricted to `is_admin(auth.uid()) = TRUE`.
- **Cart Items & Wishlists**: Enforced strictly to `auth.uid() = user_id`.
- **Orders & Order Items**: Shoppers can read and insert only their own orders (`auth.uid() = user_id`). Store administrators have system-wide read and status-update permissions.

---

## 💡 Important Decisions for Placement & System Design Interviews

1. **Why recalculate prices server-side during checkout?**
   - *Problem:* Untrusted frontend clients can tamper with JavaScript memory, DOM elements, or HTTP payloads to alter prices (e.g., changing ₹4,999 to ₹1).
   - *Solution:* SmartCart treats client price payloads as advisory only. During checkout, product IDs are fetched directly from the database and authoritative unit prices are multiplied by quantities.
2. **How is Concurrency and Stock Depletion Handled?**
   - Inventory is checked and decremented atomically during order placement. If two concurrent users attempt to buy the last unit of an item, the transaction validates stock constraints before confirming.
3. **Why use Fixed-Precision Numeric types over Float in PostgreSQL?**
   - Floating-point representations suffer from rounding errors in binary arithmetic (e.g., `0.1 + 0.2 = 0.30000000000000004`). Financial amounts are stored using `NUMERIC(10, 2)`.
4. **How are Admins Protected against Privilege Escalation?**
   - Client requests cannot grant admin access by passing `{ "role": "admin" }` in the body. The server decodes verified JWT claims and checks the profile table's `is_admin` boolean server-side via the `get_current_admin` dependency.

---

## 📤 Pushing to GitHub

Initialize git, commit, and push your repository:
```powershell
git init
git add .
git commit -m "feat: complete SmartCart e-commerce platform with FastAPI, Supabase, and Bootstrap 5"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```
