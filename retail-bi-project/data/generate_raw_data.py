"""
Generates synthetic, intentionally messy raw retail data so the ETL layer
has real cleaning work to do (duplicates, nulls, inconsistent formats).
Run once to (re)build the /data/raw files.
"""
import csv
import os
import random
from datetime import datetime, timedelta

random.seed(42)
RAW_DIR = os.path.join(os.path.dirname(__file__), "raw")
os.makedirs(RAW_DIR, exist_ok=True)

# ---------- Stores (12 locations across US regions) ----------
STORES = [
    (1, "Downtown Flagship", "New York", "NY", "Northeast"),
    (2, "Westside Mall", "Los Angeles", "CA", "West"),
    (3, "Lakeview Plaza", "Chicago", "IL", "Midwest"),
    (4, "Riverside Center", "Houston", "TX", "South"),
    (5, "Old Town Square", "Philadelphia", "PA", "Northeast"),
    (6, "Harbor Point", "Seattle", "WA", "West"),
    (7, "Sunset Boulevard", "Miami", "FL", "South"),
    (8, "Union Station Hub", "Denver", "CO", "West"),
    (9, "Peachtree Market", "Atlanta", "GA", "South"),
    (10, "Commons Galleria", "Boston", "MA", "Northeast"),
    (11, "Twin Cities Depot", "Minneapolis", "MN", "Midwest"),
    (12, "Desert Gateway", "Phoenix", "AZ", "West"),
]
with open(f"{RAW_DIR}/stores.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["store_id", "store_name", "city", "state", "region"])
    w.writerows(STORES)

# ---------- Products (8 categories, brands, subcategories) ----------
CATALOG = {
    "Electronics": {
        "brand": ["TechNova", "PulseGear", "OrbitOne"],
        "items": [
            ("Wireless Earbuds", "Audio"), ("Bluetooth Speaker", "Audio"),
            ("Phone Charger", "Accessories"), ("Smart Watch", "Wearables"),
            ("USB-C Cable", "Accessories"), ("Tablet Stand", "Accessories"),
            ("Noise-Cancel Headphones", "Audio"), ("Power Bank 20k", "Accessories"),
            ("Wireless Mouse", "Computing"), ("USB Hub 7-port", "Computing"),
        ],
    },
    "Apparel": {
        "brand": ["UrbanThread", "TrailFit", "Northloom"],
        "items": [
            ("Cotton T-Shirt", "Tops"), ("Denim Jeans", "Bottoms"),
            ("Running Shoes", "Footwear"), ("Wool Sweater", "Tops"),
            ("Rain Jacket", "Outerwear"), ("Athletic Shorts", "Bottoms"),
            ("Baseball Cap", "Accessories"), ("Hiking Boots", "Footwear"),
            ("Fleece Hoodie", "Tops"), ("Yoga Leggings", "Bottoms"),
        ],
    },
    "Home": {
        "brand": ["Hearth & Co", "Nestline", "LumenHome"],
        "items": [
            ("Ceramic Mug", "Kitchen"), ("Throw Pillow", "Living"),
            ("LED Desk Lamp", "Lighting"), ("Bath Towel Set", "Bath"),
            ("Scented Candle", "Decor"), ("Storage Baskets", "Organization"),
            ("Cookware Set", "Kitchen"), ("Area Rug 5x7", "Living"),
            ("Wall Clock", "Decor"), ("Sheet Set Queen", "Bedding"),
        ],
    },
    "Grocery": {
        "brand": ["GreenPantry", "HarvestBox", "DailyGrove"],
        "items": [
            ("Organic Coffee 12oz", "Beverages"), ("Almond Butter 16oz", "Pantry"),
            ("Sparkling Water 12pk", "Beverages"), ("Granola Bars 8pk", "Snacks"),
            ("Olive Oil 1L", "Pantry"), ("Trail Mix 1lb", "Snacks"),
            ("Green Tea 20ct", "Beverages"), ("Pasta Sauce 24oz", "Pantry"),
            ("Dark Chocolate Bar", "Snacks"), ("Honey 16oz", "Pantry"),
        ],
    },
    "Beauty": {
        "brand": ["GlowLab", "PureAura", "VelvetSkin"],
        "items": [
            ("Face Moisturizer", "Skincare"), ("Shampoo 500ml", "Hair"),
            ("Lip Balm", "Makeup"), ("Sunscreen SPF50", "Skincare"),
            ("Hand Cream", "Skincare"), ("Body Wash", "Bath"),
            ("Mascara", "Makeup"), ("Hair Conditioner", "Hair"),
            ("Face Serum", "Skincare"), ("Nail Polish Set", "Makeup"),
        ],
    },
    "Sports": {
        "brand": ["PeakMotion", "CourtPro", "Altitude"],
        "items": [
            ("Yoga Mat", "Fitness"), ("Resistance Bands", "Fitness"),
            ("Soccer Ball", "Team Sports"), ("Tennis Racket", "Racket"),
            ("Dumbbell Pair 10lb", "Fitness"), ("Water Bottle 32oz", "Accessories"),
            ("Bike Helmet", "Cycling"), ("Jump Rope", "Fitness"),
            ("Basketball", "Team Sports"), ("Gym Bag", "Accessories"),
        ],
    },
    "Toys": {
        "brand": ["PlayOrbit", "KidCraft", "WonderBox"],
        "items": [
            ("Building Blocks 100pc", "Building"), ("Board Game Classic", "Games"),
            ("Plush Bear", "Plush"), ("RC Car", "Vehicles"),
            ("Puzzle 500pc", "Puzzles"), ("Art Kit Junior", "Creative"),
            ("Action Figure", "Figures"), ("STEM Robot Kit", "STEM"),
            ("Card Game Pack", "Games"), ("Bubble Machine", "Outdoor"),
        ],
    },
    "Office": {
        "brand": ["DeskWise", "InkForge", "Paperlane"],
        "items": [
            ("Notebook A5", "Stationery"), ("Gel Pen 12pk", "Writing"),
            ("Desk Organizer", "Organization"), ("Wireless Keyboard", "Tech"),
            ("Sticky Notes 6pk", "Stationery"), ("Laptop Sleeve 15in", "Accessories"),
            ("Monitor Light Bar", "Tech"), ("File Folders 25pk", "Organization"),
            ("Highlighter Set", "Writing"), ("Ergo Desk Chair Mat", "Accessories"),
        ],
    },
}

products = []
pid = 1000
for cat, meta in CATALOG.items():
    for name, subcat in meta["items"]:
        brand = random.choice(meta["brand"])
        price = round(random.uniform(4.99, 249.99), 2)
        cost = round(price * random.uniform(0.35, 0.68), 2)
        products.append((pid, name, cat, subcat, brand, price, cost))
        pid += 1

with open(f"{RAW_DIR}/products.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["product_id", "product_name", "category", "subcategory", "brand", "unit_price", "unit_cost"])
    w.writerows(products)

# ---------- Customers (1,200) ----------
FIRST = [
    "Aisha", "Ben", "Carlos", "Deepa", "Elena", "Farid", "Grace", "Hiro", "Ines", "Jack",
    "Kira", "Liam", "Maya", "Noah", "Omar", "Priya", "Quinn", "Rosa", "Sam", "Tara",
    "Uma", "Victor", "Wendy", "Xavier", "Yara", "Zane", "Amelia", "Blake", "Chloe", "Diego",
]
LAST = [
    "Khan", "Smith", "Garcia", "Nguyen", "Patel", "Kim", "Rossi", "Muller", "Silva", "Brown",
    "Lee", "Chen", "Wilson", "Martinez", "Anderson", "Taylor", "Thomas", "Jackson", "White", "Harris",
]
SEGMENTS = ["Retail", "Loyalty", "VIP", "Wholesale", None]
customers = []
for cid in range(1, 1201):
    name = f"{random.choice(FIRST)} {random.choice(LAST)}"
    email = f"{name.lower().replace(' ', '.')}{cid}@example.com"
    signup = datetime(2021, 1, 1) + timedelta(days=random.randint(0, 1400))
    segment = random.choice(SEGMENTS)
    segment_raw = segment if segment else ""
    date_fmt = random.choice(["%Y-%m-%d", "%m/%d/%Y"])
    customers.append((cid, name, email, signup.strftime(date_fmt), segment_raw))

with open(f"{RAW_DIR}/customers.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["customer_id", "customer_name", "email", "signup_date", "segment"])
    w.writerows(customers)

# ---------- Sales transactions (~2 years, messy) ----------
PAYMENT_METHODS = ["Credit Card", "Debit Card", "Cash", "Mobile Pay", "Gift Card"]
start_date = datetime(2024, 1, 1)
n_days = 730  # 2 years
rows = []
order_id = 500000

for day in range(n_days):
    date = start_date + timedelta(days=day)
    # seasonality: weekends busier, Nov–Dec peak, summer bump
    weekend_boost = 1.35 if date.weekday() >= 5 else 1.0
    month_boost = 1.45 if date.month in (11, 12) else (1.15 if date.month in (6, 7) else 1.0)
    base = int(48 * weekend_boost * month_boost)
    n_orders = random.randint(max(20, base - 10), base + 18)

    for _ in range(n_orders):
        order_id += 1
        store_id = random.choice(STORES)[0]
        customer_id = random.randint(1, 1200)
        payment = random.choice(PAYMENT_METHODS)
        n_lines = random.randint(1, 5)
        for _ in range(n_lines):
            prod = random.choice(products)
            qty = random.randint(1, 6)
            unit_price = prod[5]
            discount = random.choice([0, 0, 0, 0, 0.05, 0.1, 0.15, 0.2, 0.25])
            date_fmt = random.choice(["%Y-%m-%d", "%m/%d/%Y", "%d-%b-%Y"])
            rows.append([
                order_id, date.strftime(date_fmt), store_id, customer_id,
                prod[0], qty, unit_price, discount, payment,
            ])

messy_rows = rows.copy()
for _ in range(400):
    messy_rows.append(random.choice(rows))
for i in random.sample(range(len(messy_rows)), 200):
    r = list(messy_rows[i])
    r[3] = ""
    messy_rows[i] = r
for i in random.sample(range(len(messy_rows)), 120):
    r = list(messy_rows[i])
    r[5] = -abs(int(r[5]))
    messy_rows[i] = r
for i in random.sample(range(len(messy_rows)), 60):
    r = list(messy_rows[i])
    r[8] = random.choice(["credit card", "DEBIT", "cash ", "mobile", ""])
    messy_rows[i] = r

with open(f"{RAW_DIR}/sales_raw.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow([
        "order_id", "order_date", "store_id", "customer_id",
        "product_id", "quantity", "unit_price", "discount_pct", "payment_method",
    ])
    w.writerows(messy_rows)

print(
    f"Generated {len(STORES)} stores, {len(products)} products, "
    f"{len(customers)} customers, {len(messy_rows)} sales line items "
    f"across {n_days} days."
)
