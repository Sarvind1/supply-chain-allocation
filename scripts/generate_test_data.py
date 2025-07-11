#!/usr/bin/env python3
"""Generate test data for allocation engine."""

import random
import pandas as pd
from pathlib import Path


def generate_products(n=100, output_file="products_generated.csv"):
    """Generate random product data."""
    categories = ["ELEC", "HOME", "TOYS", "SPRT", "BOOK", "FASH", "FOOD", "PETS", "AUTO", "GARD"]
    
    products = []
    for i in range(n):
        category = random.choice(categories)
        sku = f"{category}{str(i+1).zfill(3)}"
        
        # Generate correlated attributes
        is_oversize = 1 if random.random() < 0.2 else 0
        
        if is_oversize:
            qty = random.randint(100, 800)
            cm3 = round(random.uniform(2.5, 4.5), 2)
            volume = round(random.uniform(0.2, 0.4), 2)
            parcels = random.randint(20, 80)
        else:
            qty = random.randint(500, 4000)
            cm3 = round(random.uniform(0.3, 3.0), 2)
            volume = round(random.uniform(0.03, 0.2), 2)
            parcels = random.randint(50, 400)
        
        products.append({
            "Razin (SKU)": sku,
            "Asin": f"B{random.randint(10000000, 99999999)}",
            "Qty": qty,
            "CM3": cm3,
            "Master carton Volume": volume,
            "Is Oversize": is_oversize,
            "Parcels per MC": parcels,
            "Currency": "USD"
        })
    
    df = pd.DataFrame(products)
    df.to_csv(output_file, index=False)
    print(f"Generated {n} products to {output_file}")


if __name__ == "__main__":
    # Generate different sized datasets
    generate_products(10, "data/dummy/products_test_10.csv")
    generate_products(100, "data/dummy/products_test_100.csv")
    generate_products(1000, "data/dummy/products_test_1000.csv")