-- ==============================================================================
-- SMARTCART DEMO SEED DATA
-- Realistic Indian market catalog across Electronics, Fashion, Home Essentials & Accessories
-- ==============================================================================

-- 1. Insert Categories
INSERT INTO public.categories (id, name, slug, description, image_url) VALUES
('c1000000-0000-0000-0000-000000000001', 'Electronics & Gadgets', 'electronics', 'High-performance smart audio, wearables, and productivity accessories.', 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80'),
('c1000000-0000-0000-0000-000000000002', 'Men & Women Fashion', 'fashion', 'Contemporary streetwear, premium linen shirts, and minimalist apparel.', 'https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=800&auto=format&fit=crop&q=80'),
('c1000000-0000-0000-0000-000000000003', 'Home & Kitchen Essentials', 'home-essentials', 'Artisan ceramic tableware, ergonomic workstations, and indoor lifestyle decor.', 'https://images.unsplash.com/photo-1513519245088-0e12902e5a38?w=800&auto=format&fit=crop&q=80'),
('c1000000-0000-0000-0000-000000000004', 'Watches & Accessories', 'accessories', 'Handcrafted leather goods, precision chronograph timepieces, and travel gear.', 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80')
ON CONFLICT (slug) DO NOTHING;

-- 2. Insert Products
INSERT INTO public.products (id, category_id, name, slug, description, price, compare_at_price, image_url, stock_quantity, is_active) VALUES
-- Electronics
(
    'p1000000-0000-0000-0000-000000000001',
    'c1000000-0000-0000-0000-000000000001',
    'AuraWave Pro ANC Wireless Headphones',
    'aurawave-pro-anc-headphones',
    'Studio-grade acoustic architecture with adaptive hybrid active noise cancellation, 40-hour continuous playback, and ultra-plush memory foam earcups.',
    4999.00,
    7499.00,
    'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80',
    45,
    TRUE
),
(
    'p1000000-0000-0000-0000-000000000002',
    'c1000000-0000-0000-0000-000000000001',
    'PulseFit Horizon GPS Smartwatch',
    'pulsefit-horizon-smartwatch',
    'Aerospace-grade zinc alloy casing featuring a 1.43-inch AMOLED sunlight display, continuous SpO2 biometric monitoring, 5ATM water resistance, and built-in dual-band GPS.',
    3299.00,
    4999.00,
    'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80',
    30,
    TRUE
),
(
    'p1000000-0000-0000-0000-000000000003',
    'c1000000-0000-0000-0000-000000000001',
    'HyperKey Wireless Mechanical Keyboard',
    'hyperkey-wireless-mechanical-keyboard',
    'Compact 75% hot-swappable mechanical keyboard equipped with factory-lubed linear switches, sound-dampening silicone gasket mount, and tri-mode Bluetooth 5.2/2.4G connectivity.',
    3799.00,
    5299.00,
    'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&auto=format&fit=crop&q=80',
    25,
    TRUE
),
(
    'p1000000-0000-0000-0000-000000000004',
    'c1000000-0000-0000-0000-000000000001',
    'OmniGlide Ergonomic Precision Mouse',
    'omniglide-ergonomic-mouse',
    'Sculpted 57-degree vertical grip engineered to alleviate wrist strain. Features silent magnetic scroll wheel, multi-device flow switching, and 4000 DPI darkfield sensor.',
    1899.00,
    2499.00,
    'https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800&auto=format&fit=crop&q=80',
    50,
    TRUE
),

-- Fashion
(
    'p1000000-0000-0000-0000-000000000005',
    'c1000000-0000-0000-0000-000000000002',
    'Bespoke Pure French Linen Casual Shirt',
    'bespoke-pure-linen-shirt',
    'Spun from 100% Normandy flax fiber. Naturally breathable, pre-washed for vintage softness, featuring mother-of-pearl buttons and relaxed modern tailoring.',
    2199.00,
    3199.00,
    'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=800&auto=format&fit=crop&q=80',
    40,
    TRUE
),
(
    'p1000000-0000-0000-0000-000000000006',
    'c1000000-0000-0000-0000-000000000002',
    'UrbanKnit Heavyweight Cotton Hoodie',
    'urbanknit-heavyweight-hoodie',
    '450 GSM French terry combed cotton offering a structured drop-shoulder drape, double-layered hood, and reinforced ribbed hems.',
    2499.00,
    3499.00,
    'https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=800&auto=format&fit=crop&q=80',
    35,
    TRUE
),
(
    'p1000000-0000-0000-0000-000000000007',
    'c1000000-0000-0000-0000-000000000002',
    'Selvedge Tapered Indigo Denim Jeans',
    'selvedge-tapered-indigo-jeans',
    '13.5 oz shuttle-loom woven Japanese selvedge denim. Clean dark-indigo rope dye that ages gracefully with custom whiskers and fades.',
    2999.00,
    4299.00,
    'https://images.unsplash.com/photo-1542272604-787c3835535d?w=800&auto=format&fit=crop&q=80',
    28,
    TRUE
),

-- Home & Kitchen Essentials
(
    'p1000000-0000-0000-0000-000000000008',
    'c1000000-0000-0000-0000-000000000003',
    'Nordic Matte Ceramic Pour-Over Set',
    'nordic-ceramic-pour-over-set',
    'Handmade stoneware coffee dripper with spiral interior flow channels, wooden collar base, and 600ml borosilicate serving carafe.',
    1499.00,
    1999.00,
    'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=800&auto=format&fit=crop&q=80',
    20,
    TRUE
),
(
    'p1000000-0000-0000-0000-000000000009',
    'c1000000-0000-0000-0000-000000000003',
    'AuraGlow Ambient Minimalist Desk Lamp',
    'auraglow-minimalist-desk-lamp',
    'Sandblasted anodized aluminum housing with step-less touch dimming, 3 color temperatures (2700K-6500K), and USB-C power delivery.',
    1799.00,
    2599.00,
    'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800&auto=format&fit=crop&q=80',
    22,
    TRUE
),
(
    'p1000000-0000-0000-0000-000000000010',
    'c1000000-0000-0000-0000-000000000003',
    'Botanica Ultrasonic Aromatherapy Diffuser',
    'botanica-ultrasonic-diffuser',
    'Real bamboo wood exterior with 400ml water chamber, ultra-quiet whisper motor, automatic waterless shut-off, and subtle warm ambient illumination.',
    1299.00,
    1899.00,
    'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=800&auto=format&fit=crop&q=80',
    30,
    TRUE
),

-- Watches & Accessories
(
    'p1000000-0000-0000-0000-000000000011',
    'c1000000-0000-0000-0000-000000000004',
    'Classic Heritage Chronograph Watch',
    'classic-heritage-chronograph-watch',
    'Japanese precision quartz movement with domed sapphire crystal glass, 316L surgical stainless steel body, and genuine vegetable-tanned Italian leather band.',
    4499.00,
    6499.00,
    'https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=800&auto=format&fit=crop&q=80',
    18,
    TRUE
),
(
    'p1000000-0000-0000-0000-000000000012',
    'c1000000-0000-0000-0000-000000000004',
    'Artisan Full-Grain Leather Bi-Fold Wallet',
    'artisan-leather-bifold-wallet',
    'Hand-stitched burnished saddle leather with RFID-blocking aluminum weave lining, 6 card slots, dual cash sleeve, and minimal profile.',
    1199.00,
    1699.00,
    'https://images.unsplash.com/photo-1627123424574-724758594e93?w=800&auto=format&fit=crop&q=80',
    60,
    TRUE
)
ON CONFLICT (slug) DO UPDATE SET
    price = EXCLUDED.price,
    stock_quantity = EXCLUDED.stock_quantity;
