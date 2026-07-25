"""
seed_products.py
Optional: adds a few sample products so you can test /catalog right away.
Run once with: python seed_products.py
"""
import database as db

db.init_db()

sample_products = [
    ("Blue Ceramic Mug", "350ml, dishwasher safe", 12.50, "", "Kitchen"),
    ("Wireless Earbuds", "Bluetooth 5.0, 20hr battery", 29.99, "", "Electronics"),
    ("Cotton T-Shirt", "Unisex, sizes S-XL", 9.99, "", "Clothing"),
    ("Notebook", "A5, 120 pages, dotted grid", 4.50, "", "Stationery"),
]

for name, desc, price, image, category in sample_products:
    db.add_product(name, desc, price, image, category)

print(f"Seeded {len(sample_products)} sample products.")
