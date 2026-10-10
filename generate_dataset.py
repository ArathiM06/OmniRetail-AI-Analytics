import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_omni_retail_data(num_records=1800, seed=42):
    np.random.seed(seed)
    
    # 350 distinct customers
    customer_ids = [f"CUST{i:04d}" for i in range(1, 351)]
    customer_types = {cid: np.random.choice(["Member", "Normal"], p=[0.45, 0.55]) for cid in customer_ids}
    
    # Customer churn tendency: some customers stop buying early (churned), some are active
    # Assign an active date cutoff to each customer
    customer_lifespans = {}
    for cid in customer_ids:
        # 30% of customers churn before day 240 (Aug 2025)
        is_churner = np.random.rand() < 0.32
        if is_churner:
            max_day = np.random.randint(40, 240)
        else:
            max_day = np.random.randint(241, 450)
        customer_lifespans[cid] = max_day

    start_date = datetime(2025, 1, 1)
    
    branches = [
        ("Branch A (Mumbai)", "Mumbai"),
        ("Branch B (Bangalore)", "Bangalore"),
        ("Branch C (Delhi)", "Delhi"),
        ("Branch D (Hyderabad)", "Hyderabad")
    ]
    
    products_catalog = [
        {"Product": "Laptop Pro 15", "Category": "Electronics", "Base_Price": 58000, "Margin": 0.18},
        {"Product": "Wireless Earbuds", "Category": "Electronics", "Base_Price": 2499, "Margin": 0.35},
        {"Product": "Smart 4K TV", "Category": "Electronics", "Base_Price": 34999, "Margin": 0.22},
        {"Product": "Noise-Cancelling Headphones", "Category": "Electronics", "Base_Price": 7999, "Margin": 0.30},
        {"Product": "Organic Green Tea", "Category": "Beverages", "Base_Price": 450, "Margin": 0.45},
        {"Product": "Artisanal Coffee Beans", "Category": "Beverages", "Base_Price": 850, "Margin": 0.40},
        {"Product": "Sparkling Fruit Cider", "Category": "Beverages", "Base_Price": 320, "Margin": 0.50},
        {"Product": "Almond Milk 1L", "Category": "Beverages", "Base_Price": 280, "Margin": 0.38},
        {"Product": "Slim-Fit Denim Jeans", "Category": "Fashion", "Base_Price": 2199, "Margin": 0.42},
        {"Product": "Cotton Formal Shirt", "Category": "Fashion", "Base_Price": 1499, "Margin": 0.40},
        {"Product": "Running Sports Shoes", "Category": "Fashion", "Base_Price": 3299, "Margin": 0.35},
        {"Product": "Winter Fleece Jacket", "Category": "Fashion", "Base_Price": 3999, "Margin": 0.45},
        {"Product": "Gourmet Aged Cheddar", "Category": "Groceries", "Base_Price": 650, "Margin": 0.28},
        {"Product": "Extra Virgin Olive Oil", "Category": "Groceries", "Base_Price": 1250, "Margin": 0.25},
        {"Product": "Organic Rolled Oats", "Category": "Groceries", "Base_Price": 380, "Margin": 0.32},
        {"Product": "Wildflower Raw Honey", "Category": "Groceries", "Base_Price": 520, "Margin": 0.35},
        {"Product": "Air Fryer Deluxe", "Category": "Home & Kitchen", "Base_Price": 6499, "Margin": 0.28},
        {"Product": "Stainless Steel Cookware Set", "Category": "Home & Kitchen", "Base_Price": 4899, "Margin": 0.30},
        {"Product": "Robotic Vacuum Cleaner", "Category": "Home & Kitchen", "Base_Price": 18999, "Margin": 0.24},
        {"Product": "Hydrating Face Serum", "Category": "Beauty & Personal Care", "Base_Price": 1199, "Margin": 0.55},
        {"Product": "Sunscreen Gel SPF50", "Category": "Beauty & Personal Care", "Base_Price": 749, "Margin": 0.50},
        {"Product": "Botanical Shampoo 500ml", "Category": "Beauty & Personal Care", "Base_Price": 599, "Margin": 0.48}
    ]
    
    payment_methods = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash"]
    payment_probs = [0.42, 0.28, 0.16, 0.08, 0.06]
    
    records = []
    
    for i in range(1, num_records + 1):
        order_id = f"ORD{10000 + i}"
        
        # Pick customer
        cid = np.random.choice(customer_ids)
        c_type = customer_types[cid]
        max_day = customer_lifespans[cid]
        
        # Pick date within customer's lifespan
        day_offset = np.random.randint(0, max(1, max_day))
        order_date = start_date + timedelta(days=day_offset)
        
        # Pick branch
        branch_idx = np.random.choice([0, 1, 2, 3], p=[0.32, 0.28, 0.24, 0.16])
        branch_name, city = branches[branch_idx]
        
        # Pick item
        prod_item = np.random.choice(products_catalog)
        prod_name = prod_item["Product"]
        cat_name = prod_item["Category"]
        base_price = prod_item["Base_Price"]
        margin_pct = prod_item["Margin"]
        
        # Price variation (+/- 5%)
        unit_price = round(base_price * np.random.uniform(0.95, 1.05), 2)
        
        # Quantity
        if cat_name in ["Beverages", "Groceries"]:
            quantity = int(np.random.choice([1, 2, 3, 4, 5, 6], p=[0.25, 0.30, 0.20, 0.15, 0.06, 0.04]))
        elif cat_name == "Electronics":
            quantity = int(np.random.choice([1, 2], p=[0.88, 0.12]))
        else:
            quantity = int(np.random.choice([1, 2, 3], p=[0.60, 0.30, 0.10]))
            
        # Discount
        if c_type == "Member":
            discount_pct = np.random.choice([0.05, 0.10, 0.15, 0.20], p=[0.3, 0.4, 0.2, 0.1])
        else:
            discount_pct = np.random.choice([0.0, 0.05, 0.10], p=[0.6, 0.3, 0.1])
            
        gross_amount = round(unit_price * quantity, 2)
        discount_amount = round(gross_amount * discount_pct, 2)
        revenue = round(gross_amount - discount_amount, 2)
        profit = round(revenue * margin_pct, 2)
        
        payment_method = np.random.choice(payment_methods, p=payment_probs)
        
        # Rating (1 to 5, skewed positive)
        if c_type == "Member":
            rating = int(np.random.choice([3, 4, 5], p=[0.15, 0.45, 0.40]))
        else:
            rating = int(np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.10, 0.25, 0.40, 0.20]))
            
        records.append({
            "Order_ID": order_id,
            "Order_Date": order_date.strftime("%Y-%m-%d"),
            "Customer_ID": cid,
            "Customer_Type": c_type,
            "Branch": branch_name,
            "City": city,
            "Product": prod_name,
            "Category": cat_name,
            "Unit_Price": unit_price,
            "Quantity": quantity,
            "Discount_Pct": discount_pct,
            "Revenue": revenue,
            "Profit": profit,
            "Payment_Method": payment_method,
            "Rating": rating
        })
        
    df = pd.DataFrame(records)
    # Sort chronologically
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df = df.sort_values("Order_Date").reset_index(drop=True)
    df["Order_Date"] = df["Order_Date"].dt.strftime("%Y-%m-%d")
    
    return df

if __name__ == "__main__":
    df = generate_omni_retail_data()
    output_path = "data/omni_retail_transactions.csv"
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} records across {df['Customer_ID'].nunique()} customers.")
    print(f"Data saved to {output_path}")
    print(df.head())
