# Global Cyber Security & Data Breach Analyzer
import pandas as pd

print("Data Loading & Concatenation")
b_2024 = pd.read_csv("breaches_2024.csv")
b_2025 = pd.read_csv("breaches_2025.csv")
companies = pd.read_csv("companies.csv")

print("\nSample Records from 2024 Breaches Data:")
print(b_2024.head(3)) 

print("\nSample Records from Companies Data:")
print(companies.head(2)) 

all_breaches = pd.concat([b_2024, b_2025], ignore_index=True)
print(f"Total breach records after concatenation: {all_breaches.shape[0]}")


print("\nMerging & Data Inspection ")
b_indexed = all_breaches.set_index("Company_ID")
c_indexed = companies.set_index("Company_ID")
merged_data = b_indexed.join(c_indexed, how="inner").reset_index()

print(f"Shape of joined dataset: {merged_data.shape}")
print(f"\nColumns: {merged_data.columns.to_list()}")
print("\nData Information:")
print(merged_data.info())

print("\nFirst 5 Records (head):")
print(merged_data.head())

print("\nLast 5 Records (tail):")
print(merged_data.tail())

print("\nStatistical Summary (describe):")
print(merged_data.describe())


print("\nHandling Missing Data ")
merged_data.dropna(how="all", inplace=True)

merged_data["Breach_Date"] = pd.to_datetime(merged_data["Breach_Date"], errors="coerce")
merged_data.sort_values(by="Breach_Date", inplace=True)
merged_data.reset_index(drop=True, inplace=True)

merged_data["Financial_Loss_USD"] = merged_data["Financial_Loss_USD"].interpolate(method="linear")
merged_data["Records_Lost"] = merged_data["Records_Lost"].interpolate(method="linear")

merged_data["Records_Lost"] = merged_data["Records_Lost"].fillna(merged_data["Records_Lost"].median())
merged_data["Financial_Loss_USD"] = merged_data["Financial_Loss_USD"].fillna(merged_data["Financial_Loss_USD"].median())
merged_data["Attack_Type"] = merged_data["Attack_Type"].fillna("Unknown")

print("Missing values after cleaning:")
print(merged_data.isnull().sum())


print("\nAdd / Update / Remove Columns")
merged_data["Loss_Per_Record"] = merged_data["Financial_Loss_USD"] / merged_data["Records_Lost"].replace(0, float("nan"))
merged_data["Loss_Per_Record"] = merged_data["Loss_Per_Record"].fillna(0)
print("Added new column: 'Loss_Per_Record'")

merged_data["Priority"] = "Normal" 
merged_data.loc[merged_data["Severity_Level"] == "Critical", "Priority"] = "High Priority"
print("Added 'Priority' column. Critical attacks marked as 'High Priority'")

if "Employee_Count" in merged_data.columns:
    merged_data.drop("Employee_Count", axis=1, inplace=True)
    print("Removed unnecessary column: 'Employee_Count'")
print(f"\nUpdated Columns List: {merged_data.columns.to_list()}")


print("\nSelection, Filtering & Sorting (Ascending & Descending)")
critical_filter = (merged_data["Severity_Level"] == "Critical") & (merged_data["Records_Lost"] > 1000000)
filtered_data = merged_data[critical_filter][["Company_Name", "Attack_Type", "Records_Lost", "Financial_Loss_USD"]]

print(f"Number of massive critical attacks found: {len(filtered_data)}")
print("Top 3 massive critical attacks:")
print(filtered_data.head(3))

merged_data.sort_values(by="Company_Name", ascending=True, inplace=True)
merged_data.sort_values(by="Financial_Loss_USD", ascending=False, inplace=True)

print("\nTop 3 Breaches with Highest Financial Loss (After Sorting):")
print(merged_data[["Company_Name", "Industry", "Financial_Loss_USD"]].head(3))


print("\nAggregation & GroupBy Analysis")
print("Overall Statistics (Sum, Mean, Max, Min):")
overall_stats = merged_data[["Records_Lost", "Financial_Loss_USD"]].agg(["sum", "mean", "max", "min"])
print(overall_stats)

print("\nTotal Financial Loss by Industry:")
industry_loss = merged_data.groupby("Industry")["Financial_Loss_USD"].sum().sort_values(ascending=False)
print(industry_loss)

print("\nAverage Records Lost by Attack Type:")
attack_impact = merged_data.groupby("Attack_Type")["Records_Lost"].mean().sort_values(ascending=False)
print(attack_impact)


print("\nAdvanced Data Polishing")
merged_data["Breach_Year"] = merged_data["Breach_Date"].dt.year
merged_data["Breach_Month"] = merged_data["Breach_Date"].dt.month_name()

merged_data["Loss_Per_Record"] = merged_data["Loss_Per_Record"].round(2)
merged_data["Financial_Loss_USD"] = merged_data["Financial_Loss_USD"].round(2)
merged_data["Records_Lost"] = merged_data["Records_Lost"].round(0) 

merged_data["Status"] = merged_data["Status"].str.upper()

print("Data Polishing Successful! New columns added: 'Breach_Year', 'Breach_Month'")
print(merged_data[["Breach_Date", "Breach_Month", "Loss_Per_Record", "Status"]].head(3))
    

print("\n Exporting Final Cleaned Dataset")
merged_data.to_csv("Final_Cleaned_Breaches_Data.csv", index=False) 
print("SUCCESS: Final cleaned dataset saved as 'Final_Cleaned_Breaches_Data.csv'!")