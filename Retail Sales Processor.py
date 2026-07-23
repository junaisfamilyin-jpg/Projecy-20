import pandas as pd
import numpy as np

print("=" * 62)
print("       🛒 RETAIL SALES PROCESSOR — PANDAS DEEP DIVE")
print("=" * 62)

np.random.seed(7)

categories = ["Electronics", "Clothing", "Groceries", "Books", "Sports"]
stores = ["Store_A", "Store_B", "Store_C", "Store_D"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

records = []

for _ in range(60):
    store = np.random.choice(stores)
    category = np.random.choice(categories)
    month = np.random.choice(months)
    units = int(np.random.randint(5, 120))
    price = round(float(np.random.uniform(10, 500)), 2)
    discount = round(
        float(np.random.choice([0, 0, 0.05, 0.10, 0.15, 0.20])),
        2
    )

    records.append({
        "Store": store,
        "Category": category,
        "Month": month,
        "Units_Sold": units,
        "Unit_Price": price,
        "Discount": discount
    })

sales = pd.DataFrame(records)

print("\n📋 STEP 1 — RAW DATA SNAPSHOT")
print(f"  Shape   : {sales.shape[0]} rows × {sales.shape[1]} columns")
print(f"  Columns : {list(sales.columns)}")
print("\n  First 5 rows:")
print(sales.head().to_string(index=False))
print("\n  Data types:")

for col, dtype in sales.dtypes.items():
    print(f"    {col:<15}: {dtype}")

print("\n🧮 STEP 2 — CALCULATING REVENUE")
print("-" * 50)

sales["Gross_Revenue"] = (
    sales["Units_Sold"] * sales["Unit_Price"]
).round(2)

sales["Net_Revenue"] = (
    sales["Gross_Revenue"] * (1 - sales["Discount"])
).round(2)

sales["Discount_Amt"] = (
    sales["Gross_Revenue"] - sales["Net_Revenue"]
).round(2)

print(f"  Total Gross Revenue : ₹{sales['Gross_Revenue'].sum():>12,.2f}")
print(f"  Total Discounts     : ₹{sales['Discount_Amt'].sum():>12,.2f}")
print(f"  Total Net Revenue   : ₹{sales['Net_Revenue'].sum():>12,.2f}")
print(f"  Avg Transaction     : ₹{sales['Net_Revenue'].mean():>12,.2f}")

print("\n🏪 STEP 3 — STORE PERFORMANCE")
print("-" * 58)

store_stats = sales.groupby("Store").agg(
    Transactions=("Net_Revenue", "count"),
    Total_Revenue=("Net_Revenue", "sum"),
    Avg_Revenue=("Net_Revenue", "mean"),
    Total_Units=("Units_Sold", "sum")
).round(2)

store_stats = store_stats.sort_values(
    "Total_Revenue",
    ascending=False
)

store_stats["Rank"] = range(1, len(store_stats) + 1)

print(
    f"  {'Store':<10} {'Txns':>6} {'Total Rev':>14} "
    f"{'Avg Rev':>11} {'Units':>8} {'Rank':>5}"
)
print("  " + "-" * 56)

for store, row in store_stats.iterrows():
    print(
        f"  {store:<10} {int(row['Transactions']):>6} "
        f"₹{row['Total_Revenue']:>12,.2f} "
        f"₹{row['Avg_Revenue']:>9,.2f} "
        f"{int(row['Total_Units']):>8} "
        f"  #{int(row['Rank'])}"
    )

top_store = store_stats.index[0]

print(
    f"\n  🏆 Best performing store: {top_store} "
    f"(₹{store_stats.loc[top_store, 'Total_Revenue']:,.2f})"
)

print("\n📦 STEP 4 — CATEGORY ANALYSIS")
print("-" * 58)

cat_stats = sales.groupby("Category").agg(
    Total_Revenue=("Net_Revenue", "sum"),
    Avg_Discount=("Discount", "mean"),
    Units_Sold=("Units_Sold", "sum")
).round(2)

cat_stats["Revenue_Share_%"] = (
    cat_stats["Total_Revenue"]
    / cat_stats["Total_Revenue"].sum()
    * 100
).round(1)

cat_stats = cat_stats.sort_values(
    "Total_Revenue",
    ascending=False
)

print(
    f"  {'Category':<14} {'Total Rev':>13} "
    f"{'Rev Share':>10} {'Avg Disc':>9} {'Units':>7}"
)
print("  " + "-" * 56)

for category, row in cat_stats.iterrows():
    bar = "█" * int(row["Revenue_Share_%"] / 2)

    print(
        f"  {category:<14} ₹{row['Total_Revenue']:>11,.2f} "
        f"  {row['Revenue_Share_%']:>5.1f}%  "
        f"  {row['Avg_Discount'] * 100:>5.1f}%  "
        f"{int(row['Units_Sold']):>7}  {bar}"
    )

print("\n🔍 STEP 5 — SMART FILTERS")
print("-" * 50)

high_value = sales[
    sales["Net_Revenue"] > 5000
].sort_values(
    "Net_Revenue",
    ascending=False
)

print(f"  High-value transactions (>₹5,000): {len(high_value)}")

if len(high_value) > 0:
    print("  Top 3 high-value transactions:")

    for _, row in high_value.head(3).iterrows():
        print(
            f"    • {row['Store']} | {row['Category']} | "
            f"{row['Units_Sold']} units | ₹{row['Net_Revenue']:,.2f}"
        )

heavily_discounted = sales[
    sales["Discount"] >= 0.15
]

print(
    f"\n  Heavily discounted (≥15% off): "
    f"{len(heavily_discounted)} transactions"
)
print(
    f"  Revenue lost to discounts: "
    f"₹{heavily_discounted['Discount_Amt'].sum():,.2f}"
)
print(
    f"\n  Transactions with no discount: "
    f"{len(sales[sales['Discount'] == 0])}"
)

print("\n📊 STEP 6 — STORE × CATEGORY PIVOT")
print("-" * 62)

pivot = sales.pivot_table(
    values="Net_Revenue",
    index="Store",
    columns="Category",
    aggfunc="sum",
    fill_value=0
).round(0)

header = f"  {'Store':<10}" + "".join(
    f"{category:>14}"
    for category in pivot.columns
)

print(header)
print("  " + "-" * (10 + 14 * len(pivot.columns)))

for store in pivot.index:
    row_text = f"  {store:<10}"

    for category in pivot.columns:
        row_text += f"₹{int(pivot.loc[store, category]):>12,}"

    row_text += f"  → ₹{int(pivot.loc[store].sum()):,}"
    print(row_text)

print("\n🏆 STEP 7 — CHALLENGES")
print("-" * 62)

store_category = sales.groupby(
    ["Store", "Category"]
)["Net_Revenue"].sum()

best_combo = store_category.idxmax()
best_combo_revenue = store_category.max()

print(
    f"  1. Best store-category combo: "
    f"{best_combo[0]} + {best_combo[1]}"
)
print(f"     Revenue: ₹{best_combo_revenue:,.2f}")

sales["Cost"] = (
    sales["Units_Sold"] * sales["Unit_Price"] * 0.60
).round(2)

sales["Profit"] = (
    sales["Net_Revenue"] - sales["Cost"]
).round(2)

sales["Profit_Margin"] = (
    sales["Profit"] / sales["Net_Revenue"] * 100
).round(2)

print(
    f"\n  2. Average profit margin: "
    f"{sales['Profit_Margin'].mean():.2f}%"
)

monthly_sales = sales.groupby(
    "Month"
)["Net_Revenue"].sum().sort_values(
    ascending=False
)

best_month = monthly_sales.index[0]

print(f"\n  3. Best sales month: {best_month}")
print(f"     Revenue: ₹{monthly_sales.iloc[0]:,.2f}")

discount_revenue = sales.groupby("Category").agg(
    Total_Discount=("Discount_Amt", "sum"),
    Total_Revenue=("Net_Revenue", "sum")
)

discount_revenue["Discount_to_Revenue_Ratio"] = (
    discount_revenue["Total_Discount"]
    / discount_revenue["Total_Revenue"]
).round(4)

best_discount_category = (
    discount_revenue["Discount_to_Revenue_Ratio"].idxmin()
)

best_ratio = discount_revenue.loc[
    best_discount_category,
    "Discount_to_Revenue_Ratio"
]

print(
    f"\n  4. Best discount-to-revenue category: "
    f"{best_discount_category}"
)
print(f"     Ratio: {best_ratio:.4f}")

print("\n💾 STEP 8 — EXPORTING RESULTS")

sales.to_csv("processed_sales.csv", index=False)
store_stats.to_csv("store_summary.csv")
cat_stats.to_csv("category_summary.csv")
monthly_sales.to_csv(
    "monthly_sales.csv",
    header=["Net_Revenue"]
)
discount_revenue.to_csv(
    "discount_revenue_summary.csv"
)

print("  ✅ Saved: processed_sales.csv")
print("  ✅ Saved: store_summary.csv")
print("  ✅ Saved: category_summary.csv")
print("  ✅ Saved: monthly_sales.csv")
print("  ✅ Saved: discount_revenue_summary.csv")

print("\n" + "=" * 62)
print(f"  Total transactions analysed : {len(sales)}")
print(f"  Net revenue generated       : ₹{sales['Net_Revenue'].sum():,.2f}")
print(f"  Total profit                : ₹{sales['Profit'].sum():,.2f}")
print(f"  Best store                  : {store_stats.index[0]}")
print(f"  Best category               : {cat_stats.index[0]}")
print(f"  Best month                  : {best_month}")
print(
    f"  Best store-category combo   : "
    f"{best_combo[0]} + {best_combo[1]}"
)
print(f"  Highest single sale         : ₹{sales['Net_Revenue'].max():,.2f}")
print(f"  Most units sold in one txn  : {sales['Units_Sold'].max()}")
print("=" * 62)
