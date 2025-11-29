"""
Retail Transaction Insights - Data Analysis Project
====================================================

A comprehensive data analysis tool for a nationwide retail chain to uncover
actionable insights from transaction records. Analyzes customer behavior,
seasonal trends, promotional effectiveness, and strategic performance metrics.

Author: Data Analysis Team
Date: November 29, 2025
Version: 1.0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from collections import Counter
import warnings
import os

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# ============================================================================
# 1. CONFIGURATION & SETUP
# ============================================================================

# Set style for visualizations
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# File paths
DATASET_PATH = r'd:\IITM\python-samples\Transaction data Analysis\Retail_Transactions_Dataset.csv'
OUTPUT_DIR = r'd:\IITM\python-samples\Transaction data Analysis\analysis_output'

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================================
# 2. DATA LOADING & PREPARATION
# ============================================================================

def load_and_prepare_data(file_path):
    """
    Load CSV file and prepare data for analysis.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Cleaned and prepared dataset
    """
    print("\n" + "="*70)
    print("TASK 1: DATA PREPARATION")
    print("="*70)
    
    try:
        # Load dataset
        print(f"\n📂 Loading dataset from: {file_path}")
        df = pd.read_csv(file_path)
        print(f"✓ Dataset loaded successfully!")
        print(f"   Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
        
    except FileNotFoundError:
        print(f"✗ Error: File not found at {file_path}")
        print(f"   Please ensure 'Retail_Transactions_Dataset.csv' exists in d:\\IITM\\")
        return None
    
    # Display basic info
    print(f"\n📊 Dataset Overview:")
    print(f"   Columns: {', '.join(df.columns)}")
    print(f"   Data types:\n{df.dtypes}")
    print(f"\n   Missing values: {df.isnull().sum().sum()}")
    
    # Convert Date column to datetime
    print(f"\n🕐 Processing temporal data...")
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Extract temporal features
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Month_Name'] = df['Date'].dt.strftime('%B')
    df['DayOfWeek'] = df['Date'].dt.day_name()
    df['Week'] = df['Date'].dt.isocalendar().week
    print(f"✓ Temporal features extracted (Year, Month, DayOfWeek, Week)")
    
    # Data cleaning
    print(f"\n🧹 Cleaning data...")
    initial_rows = len(df)
    df = df.drop_duplicates()
    duplicates = initial_rows - len(df)
    print(f"   Duplicates removed: {duplicates}")
    
    # Handle missing values
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna('Unknown', inplace=True)
    
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
    
    print(f"✓ Data cleaning completed")
    print(f"   Final shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"   Missing values: {df.isnull().sum().sum()}")
    
    return df

# ============================================================================
# 3. BASIC EXPLORATION
# ============================================================================

def basic_exploration(df):
    """Perform basic exploration and summary statistics."""
    print("\n" + "="*70)
    print("TASK 2: BASIC EXPLORATION")
    print("="*70)
    
    # Transaction and customer statistics
    total_transactions = len(df)
    unique_customers = df['Customer_Name'].nunique()
    
    print(f"\n1️⃣  TRANSACTION & CUSTOMER STATISTICS")
    print(f"-" * 70)
    print(f"   Total Transactions: {total_transactions:,}")
    print(f"   Unique Customers: {unique_customers:,}")
    print(f"   Avg Transactions per Customer: {total_transactions/unique_customers:.2f}")
    
    # Top 5 products
    print(f"\n2️⃣  TOP 5 MOST COMMON PRODUCTS")
    print(f"-" * 70)
    
    products_list = []
    for products in df['Product'].dropna():
        if isinstance(products, str):
            items = [item.strip() for item in products.split(',')]
            products_list.extend(items)
    
    product_counts = Counter(products_list)
    top_5_products = pd.Series(product_counts).nlargest(5)
    
    for idx, (product, count) in enumerate(top_5_products.items(), 1):
        print(f"   {idx}. {product}: {count:,} times")
    print(f"   Total unique products: {len(product_counts)}")
    
    # Top cities
    print(f"\n3️⃣  TOP 10 CITIES BY TRANSACTION COUNT")
    print(f"-" * 70)
    
    city_transactions = df['City'].value_counts().head(10)
    for idx, (city, count) in enumerate(city_transactions.items(), 1):
        pct = (count / total_transactions) * 100
        print(f"   {idx:2}. {city:<20} {count:>6,} transactions ({pct:>5.1f}%)")
    
    # Revenue statistics
    print(f"\n4️⃣  REVENUE STATISTICS")
    print(f"-" * 70)
    print(f"   Total Revenue: ₹{df['Total_Cost'].sum():,.2f}")
    print(f"   Average Transaction: ₹{df['Total_Cost'].mean():,.2f}")
    print(f"   Median Transaction: ₹{df['Total_Cost'].median():,.2f}")
    print(f"   Min Transaction: ₹{df['Total_Cost'].min():,.2f}")
    print(f"   Max Transaction: ₹{df['Total_Cost'].max():,.2f}")
    print(f"   Std Deviation: ₹{df['Total_Cost'].std():,.2f}")
    
    print(f"\n5️⃣  ITEM STATISTICS")
    print(f"-" * 70)
    print(f"   Total Items Sold: {df['Total_Items'].sum():,}")
    print(f"   Average Items/Transaction: {df['Total_Items'].mean():.2f}")
    print(f"   Median Items/Transaction: {df['Total_Items'].median():.1f}")
    
    return {
        'total_transactions': total_transactions,
        'unique_customers': unique_customers,
        'product_counts': product_counts,
        'city_transactions': city_transactions
    }

# ============================================================================
# 4. CUSTOMER BEHAVIOUR ANALYSIS
# ============================================================================

def customer_behaviour_analysis(df):
    """Analyze customer spending patterns and preferences."""
    print("\n" + "="*70)
    print("TASK 3: CUSTOMER BEHAVIOUR ANALYSIS")
    print("="*70)
    
    # Average spending by category
    print(f"\n1️⃣  AVERAGE SPENDING BY CUSTOMER CATEGORY")
    print(f"-" * 70)
    
    spending_by_category = df.groupby('Customer_Category').agg({
        'Total_Cost': ['mean', 'sum', 'count'],
        'Total_Items': 'mean'
    }).round(2)
    
    spending_by_category.columns = ['Avg Cost', 'Total Revenue', 'Count', 'Avg Items']
    spending_by_category = spending_by_category.sort_values('Avg Cost', ascending=False)
    
    print(spending_by_category.to_string())
    max_spender = spending_by_category['Avg Cost'].idxmax()
    print(f"\n✓ Highest spending category: {max_spender} (₹{spending_by_category.loc[max_spender, 'Avg Cost']:,.2f})")
    
    # Payment method preferences
    print(f"\n2️⃣  PAYMENT METHOD PREFERENCES BY CUSTOMER CATEGORY")
    print(f"-" * 70)
    
    payment_preference = pd.crosstab(
        df['Customer_Category'],
        df['Payment_Method'],
        margins=True
    )
    print(payment_preference)
    
    # Average items by store type
    print(f"\n3️⃣  AVERAGE ITEMS PER TRANSACTION BY STORE TYPE")
    print(f"-" * 70)
    
    items_by_store = df.groupby('Store_Type').agg({
        'Total_Items': ['mean', 'median', 'sum', 'count'],
        'Total_Cost': ['mean', 'sum']
    }).round(2)
    
    items_by_store.columns = ['Avg Items', 'Median Items', 'Total Items', 'Transactions', 'Avg Cost', 'Total Revenue']
    print(items_by_store.to_string())
    
    return spending_by_category, items_by_store

# ============================================================================
# 5. PROMOTION & DISCOUNT IMPACT
# ============================================================================

def promotion_discount_analysis(df):
    """Analyze promotion and discount effectiveness."""
    print("\n" + "="*70)
    print("TASK 4: PROMOTION & DISCOUNT IMPACT ANALYSIS")
    print("="*70)
    
    # Discount impact
    print(f"\n1️⃣  IMPACT OF DISCOUNT ON TRANSACTION VALUE")
    print(f"-" * 70)
    
    discount_analysis = df.groupby('Discount_Applied').agg({
        'Total_Cost': ['mean', 'median', 'sum', 'count'],
        'Total_Items': 'mean'
    }).round(2)
    
    discount_analysis.columns = ['Avg Cost', 'Median Cost', 'Total Revenue', 'Count', 'Avg Items']
    print(discount_analysis.to_string())
    
    with_discount = df[df['Discount_Applied'] == 'Yes']['Total_Cost'].mean()
    without_discount = df[df['Discount_Applied'] == 'No']['Total_Cost'].mean()
    discount_diff = ((with_discount - without_discount) / without_discount) * 100
    
    print(f"\n   With Discount: ₹{with_discount:,.2f}")
    print(f"   Without Discount: ₹{without_discount:,.2f}")
    print(f"   Difference: {discount_diff:+.2f}%")
    
    # Promotion analysis
    print(f"\n2️⃣  AVERAGE ITEMS AND COST BY PROMOTION TYPE")
    print(f"-" * 70)
    
    promotion_analysis = df.groupby('Promotion').agg({
        'Total_Cost': ['mean', 'sum', 'count'],
        'Total_Items': 'mean'
    }).round(2)
    
    promotion_analysis.columns = ['Avg Cost', 'Total Revenue', 'Count', 'Avg Items']
    promotion_analysis = promotion_analysis.sort_values('Avg Cost', ascending=False)
    print(promotion_analysis.to_string())
    
    best_promo = promotion_analysis['Avg Cost'].idxmax()
    print(f"\n✓ Most effective promotion type: {best_promo}")
    
    return discount_diff, promotion_analysis

# ============================================================================
# 6. SEASONALITY TRENDS
# ============================================================================

def seasonality_analysis(df):
    """Analyze seasonal patterns and trends."""
    print("\n" + "="*70)
    print("TASK 5: SEASONALITY TRENDS ANALYSIS")
    print("="*70)
    
    # Revenue by season
    print(f"\n1️⃣  REVENUE ANALYSIS BY SEASON")
    print(f"-" * 70)
    
    season_analysis = df.groupby('Season').agg({
        'Total_Cost': ['sum', 'mean', 'count'],
        'Total_Items': 'mean'
    }).round(2)
    
    season_analysis.columns = ['Total Revenue', 'Avg Cost', 'Count', 'Avg Items']
    season_analysis = season_analysis.sort_values('Total Revenue', ascending=False)
    print(season_analysis.to_string())
    
    highest_season = season_analysis['Total Revenue'].idxmax()
    print(f"\n✓ Highest revenue season: {highest_season}")
    
    # Store type by season
    print(f"\n2️⃣  STORE TYPE PREFERENCES BY SEASON")
    print(f"-" * 70)
    
    season_store_analysis = df.groupby(['Season', 'Store_Type']).agg({
        'Total_Cost': ['sum', 'mean', 'count']
    }).round(2)
    
    season_store_analysis.columns = ['Total Revenue', 'Avg Cost', 'Count']
    print(season_store_analysis.to_string())
    
    # Monthly trends
    print(f"\n3️⃣  MONTHLY REVENUE TRENDS")
    print(f"-" * 70)
    
    monthly_revenue = df.groupby(['Year', 'Month', 'Month_Name']).agg({
        'Total_Cost': ['sum', 'mean', 'count']
    }).round(2)
    
    monthly_revenue.columns = ['Total Revenue', 'Avg Cost', 'Count']
    monthly_revenue = monthly_revenue.sort_index()
    print(monthly_revenue.tail(12).to_string())
    
    return season_analysis

# ============================================================================
# 7. VISUALIZATIONS
# ============================================================================

def create_visualizations(df, output_dir):
    """Create comprehensive visualization dashboard."""
    print("\n" + "="*70)
    print("TASK 6: CREATING VISUALIZATIONS")
    print("="*70)
    
    # Main Dashboard (6 panels)
    print(f"\n📊 Creating main dashboard...")
    fig = plt.figure(figsize=(16, 12))
    
    # 1. Top 10 cities
    ax1 = plt.subplot(3, 2, 1)
    top_cities = df['City'].value_counts().head(10)
    top_cities.plot(kind='bar', ax=ax1, color='steelblue')
    ax1.set_title('Top 10 Cities by Transaction Count', fontsize=12, fontweight='bold')
    ax1.set_xlabel('City')
    ax1.set_ylabel('Number of Transactions')
    ax1.tick_params(axis='x', rotation=45)
    
    # 2. Payment method pie chart
    ax2 = plt.subplot(3, 2, 2)
    payment_dist = df['Payment_Method'].value_counts()
    colors = plt.cm.Set3(range(len(payment_dist)))
    ax2.pie(payment_dist, labels=payment_dist.index, autopct='%1.1f%%', colors=colors, startangle=90)
    ax2.set_title('Distribution of Payment Methods', fontsize=12, fontweight='bold')
    
    # 3. Monthly revenue trends
    ax3 = plt.subplot(3, 2, 3)
    monthly_data = df.groupby(df['Date'].dt.to_period('M'))['Total_Cost'].sum()
    monthly_data.index = monthly_data.index.to_timestamp()
    ax3.plot(monthly_data.index, monthly_data.values, marker='o', linewidth=2, markersize=6, color='darkgreen')
    ax3.set_title('Monthly Revenue Trends', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Month')
    ax3.set_ylabel('Revenue (₹)')
    ax3.tick_params(axis='x', rotation=45)
    ax3.grid(True, alpha=0.3)
    
    # 4. Average spending by customer category
    ax4 = plt.subplot(3, 2, 4)
    customer_avg = df.groupby('Customer_Category')['Total_Cost'].mean().sort_values(ascending=False)
    customer_avg.plot(kind='bar', ax=ax4, color='coral')
    ax4.set_title('Average Spending by Customer Category', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Customer Category')
    ax4.set_ylabel('Average Cost (₹)')
    ax4.tick_params(axis='x', rotation=45)
    
    # 5. Heatmap: Revenue by season and customer category
    ax5 = plt.subplot(3, 2, 5)
    heatmap_data = df.pivot_table(values='Total_Cost', index='Season', columns='Customer_Category', aggfunc='mean')
    sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax5, cbar_kws={'label': 'Avg Cost (₹)'})
    ax5.set_title('Heatmap: Revenue by Season & Customer Category', fontsize=12, fontweight='bold')
    
    # 6. Discount impact
    ax6 = plt.subplot(3, 2, 6)
    discount_impact = df.groupby('Discount_Applied')['Total_Cost'].mean().sort_values(ascending=False)
    colors_discount = ['green', 'red']
    discount_impact.plot(kind='bar', ax=ax6, color=colors_discount)
    ax6.set_title('Average Spending: Discount Impact', fontsize=12, fontweight='bold')
    ax6.set_xlabel('Discount Applied')
    ax6.set_ylabel('Average Cost (₹)')
    ax6.tick_params(axis='x', rotation=0)
    
    plt.tight_layout()
    dashboard_path = os.path.join(output_dir, 'Retail_Dashboard.png')
    plt.savefig(dashboard_path, dpi=300, bbox_inches='tight')
    print(f"✓ Main dashboard saved: {dashboard_path}")
    plt.close()
    
    # Additional Insights (4 panels)
    print(f"📊 Creating additional insights...")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Revenue by season
    season_revenue = df.groupby('Season')['Total_Cost'].sum().sort_values(ascending=False)
    season_revenue.plot(kind='bar', ax=axes[0, 0], color='skyblue')
    axes[0, 0].set_title('Total Revenue by Season', fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('Season')
    axes[0, 0].set_ylabel('Revenue (₹)')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # 2. Average items per store type
    store_items = df.groupby('Store_Type')['Total_Items'].mean().sort_values(ascending=False)
    store_items.plot(kind='bar', ax=axes[0, 1], color='lightcoral')
    axes[0, 1].set_title('Average Items per Transaction by Store Type', fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel('Store Type')
    axes[0, 1].set_ylabel('Average Items')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # 3. Promotion effectiveness
    promo_cost = df.groupby('Promotion')['Total_Cost'].mean().sort_values(ascending=False)
    promo_cost.plot(kind='bar', ax=axes[1, 0], color='lightgreen')
    axes[1, 0].set_title('Average Cost by Promotion Type', fontsize=12, fontweight='bold')
    axes[1, 0].set_xlabel('Promotion Type')
    axes[1, 0].set_ylabel('Average Cost (₹)')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # 4. Transactions by day of week
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_transactions = df['DayOfWeek'].value_counts().reindex(day_order)
    axes[1, 1].plot(day_transactions.index, day_transactions.values, marker='o', linewidth=2, markersize=8, color='purple')
    axes[1, 1].set_title('Transactions by Day of Week', fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel('Day of Week')
    axes[1, 1].set_ylabel('Number of Transactions')
    axes[1, 1].tick_params(axis='x', rotation=45)
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    insights_path = os.path.join(output_dir, 'Additional_Insights.png')
    plt.savefig(insights_path, dpi=300, bbox_inches='tight')
    print(f"✓ Additional insights saved: {insights_path}")
    plt.close()

# ============================================================================
# 8. KEY INSIGHTS & SUMMARY
# ============================================================================

def generate_insights_summary(df, spending_by_category, items_by_store, discount_diff, promotion_analysis, season_analysis):
    """Generate and display key insights."""
    print("\n" + "="*70)
    print("TASK 7: KEY INSIGHTS & RECOMMENDATIONS")
    print("="*70)
    
    # 1. Customer spending patterns
    print(f"\n1️⃣  CUSTOMER SPENDING PATTERNS")
    print(f"-" * 70)
    top_category = spending_by_category['Avg Cost'].idxmax()
    top_category_value = spending_by_category.loc[top_category, 'Avg Cost']
    total_transactions = len(df)
    unique_customers = df['Customer_Name'].nunique()
    
    print(f"   • {top_category} customers spend the most (₹{top_category_value:,.2f} avg)")
    print(f"   • Total transactions analyzed: {total_transactions:,}")
    print(f"   • Unique customers in dataset: {unique_customers:,}")
    print(f"   • Overall average transaction value: ₹{df['Total_Cost'].mean():,.2f}")
    print(f"   📌 Recommendation: Focus marketing on {top_category} segment")
    
    # 2. Promotion effectiveness
    print(f"\n2️⃣  PROMOTION EFFECTIVENESS")
    print(f"-" * 70)
    best_promo = promotion_analysis['Avg Cost'].idxmax()
    best_promo_value = promotion_analysis.loc[best_promo, 'Avg Cost']
    print(f"   • Most effective promotion: {best_promo} (₹{best_promo_value:,.2f} avg spending)")
    print(f"   • Discount impact: {discount_diff:+.2f}% change in transaction value")
    if discount_diff < 0:
        print(f"   ⚠️  Discounts reduce average transaction value")
    else:
        print(f"   ✓ Discounts increase average transaction value")
    print(f"   📌 Recommendation: Prioritize {best_promo} promotions")
    
    # 3. Seasonal performance
    print(f"\n3️⃣  SEASONAL PERFORMANCE")
    print(f"-" * 70)
    highest_season = season_analysis['Total Revenue'].idxmax()
    highest_season_revenue = season_analysis.loc[highest_season, 'Total Revenue']
    lowest_season = season_analysis['Total Revenue'].idxmin()
    lowest_season_revenue = season_analysis.loc[lowest_season, 'Total Revenue']
    seasonal_diff = ((highest_season_revenue - lowest_season_revenue) / lowest_season_revenue) * 100
    
    print(f"   • Peak season: {highest_season} (₹{highest_season_revenue:,.2f} total revenue)")
    print(f"   • Lowest season: {lowest_season} (₹{lowest_season_revenue:,.2f} total revenue)")
    print(f"   • Seasonal variance: {seasonal_diff:.1f}% difference")
    print(f"   📌 Recommendation: Increase inventory for {highest_season}")
    
    # 4. Store type performance
    print(f"\n4️⃣  STORE TYPE INSIGHTS")
    print(f"-" * 70)
    best_store = items_by_store['Avg Items'].idxmax()
    best_store_items = items_by_store.loc[best_store, 'Avg Items']
    print(f"   • Highest basket size: {best_store} ({best_store_items:.2f} items per transaction)")
    print(f"   • Total store types: {df['Store_Type'].nunique()}")
    print(f"   📌 Recommendation: Use {best_store} format for bulk purchases")
    
    # 5. Payment preferences
    print(f"\n5️⃣  PAYMENT METHOD TRENDS")
    print(f"-" * 70)
    top_payment = df['Payment_Method'].value_counts().index[0]
    top_payment_pct = (df['Payment_Method'].value_counts().iloc[0] / len(df)) * 100
    print(f"   • Most used payment method: {top_payment} ({top_payment_pct:.1f}% of transactions)")
    print(f"   • Total payment methods: {df['Payment_Method'].nunique()}")
    print(f"   📌 Recommendation: Ensure {top_payment} is always available")
    
    # 6. Geographic insights
    print(f"\n6️⃣  GEOGRAPHIC INSIGHTS")
    print(f"-" * 70)
    top_city = df['City'].value_counts().index[0]
    top_city_transactions = df['City'].value_counts().iloc[0]
    top_city_pct = (top_city_transactions / len(df)) * 100
    print(f"   • Leading city: {top_city} ({top_city_transactions:,} transactions, {top_city_pct:.1f}%)")
    print(f"   • Total cities covered: {df['City'].nunique()}")
    print(f"   📌 Recommendation: Expand operations in underperforming cities")

# ============================================================================
# 9. FINAL SUMMARY
# ============================================================================

def generate_final_summary(df):
    """Generate final summary statistics."""
    print("\n" + "="*70)
    print("FINAL SUMMARY STATISTICS")
    print("="*70)
    
    products_list = []
    for products in df['Product'].dropna():
        if isinstance(products, str):
            items = [item.strip() for item in products.split(',')]
            products_list.extend(items)
    
    discount_count = df['Discount_Applied'].value_counts().get('Yes', 0)
    discount_rate = (discount_count / len(df)) * 100
    
    summary_data = {
        'Metric': [
            'Total Transactions',
            'Unique Customers',
            'Total Revenue',
            'Average Transaction Value',
            'Total Items Sold',
            'Average Items per Transaction',
            'Unique Products',
            'Cities Covered',
            'Store Types',
            'Payment Methods',
            'Customer Categories',
            'Promotion Types',
            'Discount Usage Rate'
        ],
        'Value': [
            f"{len(df):,}",
            f"{df['Customer_Name'].nunique():,}",
            f"₹{df['Total_Cost'].sum():,.2f}",
            f"₹{df['Total_Cost'].mean():,.2f}",
            f"{df['Total_Items'].sum():,}",
            f"{df['Total_Items'].mean():.2f}",
            f"{len(set(products_list))}",
            f"{df['City'].nunique()}",
            f"{df['Store_Type'].nunique()}",
            f"{df['Payment_Method'].nunique()}",
            f"{df['Customer_Category'].nunique()}",
            f"{df['Promotion'].nunique()}",
            f"{discount_rate:.1f}%"
        ]
    }
    
    summary_df = pd.DataFrame(summary_data)
    print("\n" + summary_df.to_string(index=False))
    print("\n" + "="*70)

# ============================================================================
# 10. MAIN EXECUTION
# ============================================================================

def main():
    """Execute the complete analysis."""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  RETAIL TRANSACTION INSIGHTS - DATA ANALYSIS PROJECT".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    # Load and prepare data
    df = load_and_prepare_data(DATASET_PATH)
    if df is None:
        return
    
    # Perform analyses
    exploration_results = basic_exploration(df)
    spending_by_category, items_by_store = customer_behaviour_analysis(df)
    discount_diff, promotion_analysis = promotion_discount_analysis(df)
    season_analysis = seasonality_analysis(df)
    
    # Create visualizations
    create_visualizations(df, OUTPUT_DIR)
    
    # Generate insights
    generate_insights_summary(df, spending_by_category, items_by_store, discount_diff, promotion_analysis, season_analysis)
    
    # Final summary
    generate_final_summary(df)
    
    print("\n✅ ANALYSIS COMPLETE!")
    print(f"\n📁 Output files saved to: {OUTPUT_DIR}")
    print(f"   • Retail_Dashboard.png")
    print(f"   • Additional_Insights.png")
    
    print("\n" + "="*70)
    print("Thank you for using Retail Transaction Insights!")
    print("="*70 + "\n")

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
