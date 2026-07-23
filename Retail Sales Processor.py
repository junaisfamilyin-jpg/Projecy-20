import pandas as pd
import numpy as np

np.random.seed(10)

stores = ["Store_A", "Store_B", "Store_C", "Store_D"]
categories = ["Electronics", "Clothing", "Food", "Home", "Sports"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

data = {
    "Store": np.random.choice(stores, 60),
    "Category": np.random.choice(categories, 60),
    "Month": np.random.choice(months, 60),
    "Units_Sold": np.random.randint(1, 101, 60),
    "Unit_Price": np.round(np.random.uniform(5, 500, 60), 2),
    "Discount": np.random.choice([0, 0.05, 0.10, 0.15, 0.20], 60)
}

sales = pd.DataFrame(data)

sales["Gross_Revenue"] = sales["Units_Sold"] * sales["Unit_Price"]
sales["Final_Revenue"] = sales["Gross_Revenue"] * (1 - sales["Discount"])

sales["Gross_Revenue"] = sales["Gross_Revenue"].round(2)
sales["Final_Revenue"] = sales["Final_Revenue"].round(2)

print("Retail Sales Data")
print(sales)

filtered_sales = sales[
    (sales["Final_Revenue"] > 5000) &
    (sales["Discount"] <= 0.10)
]

filtered_sales = filtered_sales.sort_values(
    by="Final_Revenue",
    ascending=False
)

print("\nFiltered and Sorted Sales")
print(filtered_sales)

store_results = sales.groupby("Store").agg(
    Total_Units=("Units_Sold", "sum"),
    Total_Revenue=("Final_Revenue", "sum"),
    Average_Revenue=("Final_Revenue", "mean")
).round(2)

store_results = store_results.sort_values(
    by="Total_Revenue",
    ascending=False
)

print("\nStore Results")
print(store_results)

category_results = sales.groupby("Category").agg(
    Total_Units=("Units_Sold", "sum"),
    Total_Revenue=("Final_Revenue", "sum"),
    Average_Price=("Unit_Price", "mean")
).round(2)

category_results = category_results.sort_values(
    by="Total_Revenue",
    ascending=False
)

print("\nCategory Results")
print(category_results)

top_store = store_results.index[0]
top_category = category_results.index[0]

print("\nTop Store:", top_store)
print("Top Category:", top_category)


def sale_level(revenue):
    if revenue >= 20000:
        return "High"
    elif revenue >= 5000:
        return "Medium"
    else:
        return "Low"


sales["Sale_Level"] = sales["Final_Revenue"].apply(sale_level)

print("\nSales With Levels")
print(sales)

sales.to_csv("retail_sales.csv", index=False)
