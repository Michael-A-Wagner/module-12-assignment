# Module 12 Assignment: Business Analytics Fundamentals and Applications
# GreenGrocer Data Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Welcome message
print("=" * 60)
print("GREENGROCER BUSINESS ANALYTICS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Set seed for reproducibility
np.random.seed(42)

# Store information
stores = ["Tampa", "Orlando", "Miami", "Jacksonville", "Gainesville"]
store_data = {
    "Store": stores,
    "SquareFootage": [15000, 12000, 18000, 10000, 8000],
    "StaffCount": [45, 35, 55, 30, 25],
    "YearsOpen": [5, 3, 7, 2, 1],
    "WeeklyMarketingSpend": [2500, 2000, 3000, 1800, 1500]
}

# Create store dataframe
store_df = pd.DataFrame(store_data)

# Product categories and departments
departments = ["Produce", "Dairy", "Bakery", "Grocery", "Prepared Foods"]
categories = {
    "Produce": ["Organic Vegetables", "Organic Fruits", "Fresh Herbs"],
    "Dairy": ["Milk & Cream", "Cheese", "Yogurt"],
    "Bakery": ["Bread", "Pastries", "Cakes"],
    "Grocery": ["Grains", "Canned Goods", "Snacks"],
    "Prepared Foods": ["Hot Bar", "Salad Bar", "Sandwiches"]
}

# Generate sales data for each store
sales_data = []
dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")

# Base performance factors for each store (relative scale)
store_performance = {
    "Tampa": 1.0, 
    "Orlando": 0.85, 
    "Miami": 1.2, 
    "Jacksonville": 0.75, 
    "Gainesville": 0.65
}

# Base performance factors for each department (relative scale)
dept_performance = {
    "Produce": 1.2,
    "Dairy": 1.0,
    "Bakery": 0.85,
    "Grocery": 0.95,
    "Prepared Foods": 1.1
}

# Generate daily sales data for each store, department, and category
for date in dates:
    # Seasonal factor (higher in summer and December)
    month = date.month
    seasonal_factor = 1.0
    if month in [6, 7, 8]:  # Summer
        seasonal_factor = 1.15
    elif month == 12:  # December
        seasonal_factor = 1.25
    elif month in [1, 2]:  # Winter
        seasonal_factor = 0.9
    
    # Day of week factor (weekends are busier)
    dow_factor = 1.3 if date.dayofweek >= 5 else 1.0  # Weekend vs weekday
    
    for store in stores:
        store_factor = store_performance[store]
        
        for dept in departments:
            dept_factor = dept_performance[dept]
            
            for category in categories[dept]:
                # Base sales amount
                base_sales = np.random.normal(loc=500, scale=100)
                
                # Calculate final sales with all factors and some randomness
                sales_amount = base_sales * store_factor * dept_factor * seasonal_factor * dow_factor
                sales_amount = sales_amount * np.random.normal(loc=1.0, scale=0.1)  # Add noise
                
                # Calculate profit margin (different base margins for departments)
                base_margin = {
                    "Produce": 0.25,
                    "Dairy": 0.22,
                    "Bakery": 0.35,
                    "Grocery": 0.20,
                    "Prepared Foods": 0.40
                }[dept]
                profit_margin = base_margin * np.random.normal(loc=1.0, scale=0.05)
                profit_margin = max(min(profit_margin, 0.5), 0.15)  # Keep within reasonable range
                
                # Calculate profit
                profit = sales_amount * profit_margin
                
                # Add record
                sales_data.append({
                    "Date": date,
                    "Store": store,
                    "Department": dept,
                    "Category": category,
                    "Sales": round(sales_amount, 2),
                    "ProfitMargin": round(profit_margin, 4),
                    "Profit": round(profit, 2)
                })

# Create sales dataframe
sales_df = pd.DataFrame(sales_data)

# Generate customer data
customer_data = []
total_customers = 5000

# Age distribution parameters
age_mean, age_std = 42, 15

# Income distribution parameters (in $1000s)
income_mean, income_std = 85, 30

# Create customer segments (will indirectly influence spending)
segments = ["Health Enthusiast", "Gourmet Cook", "Family Shopper", "Budget Organic", "Occasional Visitor"]
segment_probabilities = [0.25, 0.20, 0.30, 0.15, 0.10]

# Store preference probabilities (matches store performance somewhat)
store_probs = {
    "Tampa": 0.25,
    "Orlando": 0.20,
    "Miami": 0.30,
    "Jacksonville": 0.15,
    "Gainesville": 0.10
}

for i in range(total_customers):
    # Basic demographics
    age = int(np.random.normal(loc=age_mean, scale=age_std))
    age = max(min(age, 85), 18)  # Keep age in reasonable range
    
    gender = np.random.choice(["M", "F"], p=[0.48, 0.52])
    
    income = int(np.random.normal(loc=income_mean, scale=income_std))
    income = max(income, 20)  # Minimum income
    
    # Customer segment
    segment = np.random.choice(segments, p=segment_probabilities)
    
    # Preferred store
    preferred_store = np.random.choice(stores, p=list(store_probs.values()))
    
    # Shopping behavior - influenced by segment
    if segment == "Health Enthusiast":
        visit_frequency = np.random.randint(8, 15)  # Visits per month
        avg_basket = np.random.normal(loc=75, scale=15)
    elif segment == "Gourmet Cook":
        visit_frequency = np.random.randint(4, 10)
        avg_basket = np.random.normal(loc=120, scale=25)
    elif segment == "Family Shopper":
        visit_frequency = np.random.randint(5, 12)
        avg_basket = np.random.normal(loc=150, scale=30)
    elif segment == "Budget Organic":
        visit_frequency = np.random.randint(6, 10)
        avg_basket = np.random.normal(loc=60, scale=10)
    else:  # Occasional Visitor
        visit_frequency = np.random.randint(1, 5)
        avg_basket = np.random.normal(loc=45, scale=15)
    
    # Ensure values are reasonable
    visit_frequency = max(min(visit_frequency, 30), 1)
    avg_basket = max(avg_basket, 15)
    
    # Loyalty tier based on combination of frequency and spending
    monthly_spend = visit_frequency * avg_basket
    if monthly_spend > 1000:
        loyalty_tier = "Platinum"
    elif monthly_spend > 500:
        loyalty_tier = "Gold"
    elif monthly_spend > 200:
        loyalty_tier = "Silver"
    else:
        loyalty_tier = "Bronze"
    
    # Add to customer data
    customer_data.append({
        "CustomerID": f"C{i+1:04d}",
        "Age": age,
        "Gender": gender,
        "Income": income * 1000,  # Convert to actual income
        "Segment": segment,
        "PreferredStore": preferred_store,
        "VisitsPerMonth": visit_frequency,
        "AvgBasketSize": round(avg_basket, 2),
        "MonthlySpend": round(visit_frequency * avg_basket, 2),
        "LoyaltyTier": loyalty_tier
    })

# Create customer dataframe
customer_df = pd.DataFrame(customer_data)

# Create some calculated operational metrics for stores
operational_data = []

for store in stores:
    # Get store details
    store_row = store_df[store_df["Store"] == store].iloc[0]
    square_footage = store_row["SquareFootage"]
    staff_count = store_row["StaffCount"]
    
    # Calculate store metrics
    store_sales = sales_df[sales_df["Store"] == store]["Sales"].sum()
    store_profit = sales_df[sales_df["Store"] == store]["Profit"].sum()
    
    # Calculate derived metrics
    sales_per_sqft = store_sales / square_footage
    profit_per_sqft = store_profit / square_footage
    sales_per_staff = store_sales / staff_count
    inventory_turnover = np.random.uniform(12, 18) * store_performance[store]
    customer_satisfaction = min(5, np.random.normal(loc=4.0, scale=0.3) * 
                                (store_performance[store] ** 0.5))
    
    # Add to operational data
    operational_data.append({
        "Store": store,
        "AnnualSales": round(store_sales, 2),
        "AnnualProfit": round(store_profit, 2),
        "SalesPerSqFt": round(sales_per_sqft, 2),
        "ProfitPerSqFt": round(profit_per_sqft, 2),
        "SalesPerStaff": round(sales_per_staff, 2),
        "InventoryTurnover": round(inventory_turnover, 2),
        "CustomerSatisfaction": round(customer_satisfaction, 2)
    })

# Create operational dataframe
operational_df = pd.DataFrame(operational_data)

# Print data info
print("\nDataframes created successfully. Ready for analysis!")
print(f"Sales data shape: {sales_df.shape}")
print(f"Customer data shape: {customer_df.shape}")
print(f"Store data shape: {store_df.shape}")
print(f"Operational data shape: {operational_df.shape}")

# Print sample of each dataframe
print("\nSales Data Sample:")
print(sales_df.head(3))
print("\nCustomer Data Sample:")
print(customer_df.head(3))
print("\nStore Data Sample:")
print(store_df)
print("\nOperational Data Sample:")
print(operational_df)
# ----- END OF DATA CREATION -----

# TODO 1: Descriptive Analytics - Overview of Current Performance
# 1.1 Calculate and display basic descriptive statistics for sales and profit
# REQUIRED: Store results in variables for testing
def analyze_sales_performance():
    """
    Analyze overall sales performance with descriptive statistics
    REQUIRED: Create and return dictionary with keys:
    - 'total_sales': float
    - 'total_profit': float
    - 'avg_profit_margin': float
    - 'sales_by_store': pandas Series
    - 'sales_by_dept': pandas Series
    """
    total_sales = sales_df["Sales"].sum()
    total_profit = sales_df["Profit"].sum()
    # Weighted average profit margin by sales
    avg_profit_margin = (sales_df["Profit"].sum() / sales_df["Sales"].sum())

    sales_by_store = sales_df.groupby("Store")["Sales"].sum().sort_values(ascending=False)
    sales_by_dept = sales_df.groupby("Department")["Sales"].sum().sort_values(ascending=False)

    print(f"Total Sales: ${total_sales:,.2f}")
    print(f"Total Profit: ${total_profit:,.2f}")
    print(f"Average Profit Margin: {avg_profit_margin:.2%}")
    print("\nSales by Store:")
    print(sales_by_store)
    print("\nSales by Department:")
    print(sales_by_dept)

    return {
        "total_sales": float(total_sales),
        "total_profit": float(total_profit),
        "avg_profit_margin": float(avg_profit_margin),
        "sales_by_store": sales_by_store,
        "sales_by_dept": sales_by_dept
    }

# 1.2 Create visualizations showing sales distribution by store, department, and time
# REQUIRED: Return matplotlib figures
def visualize_sales_distribution():
    """
    Create visualizations showing how sales are distributed
    REQUIRED: Return tuple of three figures (store_fig, dept_fig, time_fig)
    """
    # Sales by store
    store_sales = sales_df.groupby("Store")["Sales"].sum()
    store_fig = plt.figure(figsize=(6, 4))
    store_sales.plot(kind="bar", color="seagreen")
    plt.title("Total Sales by Store")
    plt.ylabel("Sales ($)")
    plt.xlabel("Store")
    plt.tight_layout()

    # Sales by department
    dept_sales = sales_df.groupby("Department")["Sales"].sum()
    dept_fig = plt.figure(figsize=(6, 4))
    dept_sales.plot(kind="bar", color="steelblue")
    plt.title("Total Sales by Department")
    plt.ylabel("Sales ($)")
    plt.xlabel("Department")
    plt.tight_layout()

    # Sales over time (monthly)
    time_series = sales_df.groupby("Date")["Sales"].sum().resample("M").sum()
    time_fig = plt.figure(figsize=(8, 4))
    time_series.plot(marker="o")
    plt.title("Monthly Sales Trend")
    plt.ylabel("Sales ($)")
    plt.xlabel("Month")
    plt.tight_layout()

    return store_fig, dept_fig, time_fig

# 1.3 Analyze customer segments and their spending patterns
# REQUIRED: Return analysis results
def analyze_customer_segments():
    """
    Analyze customer segments and their relationship to spending
    REQUIRED: Return dictionary with keys:
    - 'segment_counts': pandas Series
    - 'segment_avg_spend': pandas Series
    - 'segment_loyalty': pandas DataFrame
    """
    segment_counts = customer_df["Segment"].value_counts()
    segment_avg_spend = customer_df.groupby("Segment")["MonthlySpend"].mean().sort_values(ascending=False)
    segment_loyalty = pd.crosstab(customer_df["Segment"], customer_df["LoyaltyTier"])

    print("\nCustomer Segment Counts:")
    print(segment_counts)
    print("\nAverage Monthly Spend by Segment:")
    print(segment_avg_spend)
    print("\nSegment vs Loyalty Tier:")
    print(segment_loyalty)

    return {
        "segment_counts": segment_counts,
        "segment_avg_spend": segment_avg_spend,
        "segment_loyalty": segment_loyalty
    }


# TODO 2: Diagnostic Analytics - Understanding Relationships
# 2.1 Identify factors correlated with sales performance
# REQUIRED: Return correlation results
def analyze_sales_correlations():
    """
    Analyze correlations between various factors and sales performance
    REQUIRED: Return dictionary with keys:
    - 'store_correlations': pandas DataFrame
    - 'top_correlations': list of tuples (factor, correlation)
    - 'correlation_fig': matplotlib figure
    """
    # Merge store characteristics with performance metrics
    store_merged = store_df.merge(operational_df, on="Store", how="inner")

    # Select numeric columns only
    numeric_cols = store_merged.select_dtypes(include=[np.number])

    # Full correlation matrix
    store_correlations = numeric_cols.corr()

    # Correlations with AnnualSales (drop self-correlation)
    sales_corr = store_correlations["AnnualSales"].drop(labels=["AnnualSales"])

    # Sort by absolute magnitude, highest first
    sales_corr_sorted = sales_corr.reindex(sales_corr.abs().sort_values(ascending=False).index)

    # Select top correlations (at least 1 required)
    top_correlations = list(sales_corr_sorted.head(5).items())

    # Create heatmap figure
    correlation_fig = plt.figure(figsize=(8, 6))
    plt.imshow(store_correlations, cmap="coolwarm", vmin=-1, vmax=1)
    plt.colorbar(label="Correlation")
    plt.xticks(range(len(store_correlations.columns)), store_correlations.columns, rotation=45, ha="right")
    plt.yticks(range(len(store_correlations.index)), store_correlations.index)
    plt.title("Correlation Matrix - Store Metrics")
    plt.tight_layout()

    return {
        "store_correlations": store_correlations,
        "top_correlations": top_correlations,
        "correlation_fig": correlation_fig
    }

# 2.2 Compare stores based on operational metrics
# REQUIRED: Return comparison results
def compare_store_performance():
    """
    Compare stores across different operational metrics
    REQUIRED: Return dictionary with keys:
    - 'efficiency_metrics': pandas DataFrame (with SalesPerSqFt, SalesPerStaff)
    - 'performance_ranking': pandas Series (ranked by profit)
    - 'comparison_fig': matplotlib figure
    """
    efficiency_metrics = operational_df.set_index("Store")[["SalesPerSqFt", "SalesPerStaff"]]

    performance_ranking = operational_df.set_index("Store")["AnnualProfit"].rank(
        ascending=False, method="dense"
    )

    comparison_fig = plt.figure(figsize=(6, 4))
    operational_df.set_index("Store")["AnnualProfit"].sort_values().plot(kind="bar", color="darkorange")
    plt.title("Annual Profit by Store")
    plt.ylabel("Profit ($)")
    plt.xlabel("Store")
    plt.tight_layout()

    print("\nEfficiency Metrics (Sales per SqFt, Sales per Staff):")
    print(efficiency_metrics)
    print("\nStore Performance Ranking by Profit (1 = highest):")
    print(performance_ranking.sort_values())

    return {
        "efficiency_metrics": efficiency_metrics,
        "performance_ranking": performance_ranking,
        "comparison_fig": comparison_fig
    }

# 2.3 Analyze seasonal patterns and their impact
# REQUIRED: Return seasonal analysis
def analyze_seasonal_patterns():
    """
    Identify and visualize seasonal patterns in sales data
    REQUIRED: Return dictionary with keys:
    - 'monthly_sales': pandas Series
    - 'dow_sales': pandas Series (day of week)
    - 'seasonal_fig': matplotlib figure
    """
    monthly_sales = sales_df.groupby(sales_df["Date"].dt.to_period("M"))["Sales"].sum()
    dow_sales = sales_df.groupby(sales_df["Date"].dt.dayofweek)["Sales"].sum()
    dow_sales.index = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    seasonal_fig = plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    monthly_sales.plot(marker="o")
    plt.title("Monthly Sales")
    plt.xlabel("Month")
    plt.ylabel("Sales ($)")

    plt.subplot(1, 2, 2)
    dow_sales.plot(kind="bar", color="mediumpurple")
    plt.title("Sales by Day of Week")
    plt.xlabel("Day of Week")
    plt.ylabel("Sales ($)")
    plt.tight_layout()

    print("\nMonthly Sales:")
    print(monthly_sales)
    print("\nSales by Day of Week:")
    print(dow_sales)

    return {
        "monthly_sales": monthly_sales,
        "dow_sales": dow_sales,
        "seasonal_fig": seasonal_fig
    }


# TODO 3: Predictive Analytics - Basic Forecasting
# 3.1 Create a simple linear regression model to predict store sales
# REQUIRED: Return model results
def predict_store_sales():
    """
    Use linear regression to predict store sales based on store characteristics
    REQUIRED: Return dictionary with keys:
    - 'coefficients': dict (feature: coefficient)
    - 'r_squared': float
    - 'predictions': pandas Series
    - 'model_fig': matplotlib figure
    """
    # Features from store_df, target from operational_df
    merged = store_df.merge(operational_df[["Store", "AnnualSales"]], on="Store", how="inner")
    feature_cols = ["SquareFootage", "StaffCount", "YearsOpen", "WeeklyMarketingSpend"]

    X = merged[feature_cols].values.astype(float)
    y = merged["AnnualSales"].values.astype(float)

    # Add intercept
    X_design = np.column_stack([np.ones(X.shape[0]), X])

    # Linear regression using least squares
    beta, _, _, _ = np.linalg.lstsq(X_design, y, rcond=None)
    intercept = beta[0]
    coefs = beta[1:]

    y_pred = X_design @ beta

    # R-squared
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot != 0 else 0.0

    coefficients = {"Intercept": float(intercept)}
    for name, c in zip(feature_cols, coefs):
        coefficients[name] = float(c)

    predictions = pd.Series(y_pred, index=merged["Store"], name="PredictedSales")

    model_fig = plt.figure(figsize=(5, 5))
    plt.scatter(y, y_pred, color="teal")
    max_val = max(y.max(), y_pred.max())
    min_val = min(y.min(), y_pred.min())
    plt.plot([min_val, max_val], [min_val, max_val], "r--")
    plt.xlabel("Actual Annual Sales")
    plt.ylabel("Predicted Annual Sales")
    plt.title(f"Store Sales Prediction (R² = {r_squared:.2f})")
    plt.tight_layout()

    print("\nRegression Coefficients for Store Sales Prediction:")
    for k, v in coefficients.items():
        print(f"{k}: {v:.4f}")
    print(f"R-squared: {r_squared:.3f}")

    return {
        "coefficients": coefficients,
        "r_squared": float(r_squared),
        "predictions": predictions,
        "model_fig": model_fig
    }

# 3.2 Forecast departmental sales trends
# REQUIRED: Return forecast results
def forecast_department_sales():
    """
    Analyze and forecast departmental sales trends
    REQUIRED: Return dictionary with keys:
    - 'dept_trends': pandas DataFrame
    - 'growth_rates': pandas Series
    - 'forecast_fig': matplotlib figure
    """
    # Monthly sales by department
    dept_monthly = (
        sales_df
        .groupby([sales_df["Date"].dt.to_period("M"), "Department"])["Sales"]
        .sum()
        .reset_index()
    )
    # Convert period to integer index for trend
    dept_monthly["MonthIndex"] = dept_monthly["Date"].astype(str).rank(method="dense").astype(int)

    trend_rows = []
    for dept in dept_monthly["Department"].unique():
        sub = dept_monthly[dept_monthly["Department"] == dept]
        x = sub["MonthIndex"].values.astype(float)
        y = sub["Sales"].values.astype(float)
        slope, intercept, _, _, _ = stats.linregress(x, y)
        trend_rows.append({"Department": dept, "Slope": slope, "Intercept": intercept})

    dept_trends = pd.DataFrame(trend_rows).set_index("Department")
    growth_rates = dept_trends["Slope"]

    forecast_fig = plt.figure(figsize=(8, 5))
    for dept in dept_monthly["Department"].unique():
        sub = dept_monthly[dept_monthly["Department"] == dept]
        plt.plot(sub["Date"].astype(str), sub["Sales"], marker="o", label=dept)
    plt.xticks(rotation=45, ha="right")
    plt.title("Monthly Department Sales Trends")
    plt.ylabel("Sales ($)")
    plt.xlabel("Month")
    plt.legend()
    plt.tight_layout()

    print("\nDepartment Sales Trends (Slope indicates growth rate):")
    print(dept_trends)

    return {
        "dept_trends": dept_trends,
        "growth_rates": growth_rates,
        "forecast_fig": forecast_fig
    }


# TODO 4: Integrated Analysis - Business Insights and Recommendations
# 4.1 Identify the most profitable combinations of store, department, and customer segments
# REQUIRED: Return opportunity analysis
def identify_profit_opportunities():
    """
    Identify the most profitable combinations and potential opportunities
    REQUIRED: Return dictionary with keys:
    - 'top_combinations': pandas DataFrame (top 10 store-dept combinations)
    - 'underperforming': pandas DataFrame (bottom 10)
    - 'opportunity_score': pandas Series (by store)
    """
    # Profit by store and department
    store_dept_profit = (
        sales_df.groupby(["Store", "Department"])["Profit"]
        .sum()
        .reset_index()
        .sort_values("Profit", ascending=False)
    )

    top_combinations = store_dept_profit.head(10).reset_index(drop=True)
    underperforming = store_dept_profit.tail(10).reset_index(drop=True)

    # Opportunity score: combine profit per sqft and customer satisfaction
    opp_df = operational_df.set_index("Store")
    # Normalize metrics
    sales_sq_norm = (opp_df["SalesPerSqFt"] - opp_df["SalesPerSqFt"].mean()) / opp_df["SalesPerSqFt"].std()
    profit_sq_norm = (opp_df["ProfitPerSqFt"] - opp_df["ProfitPerSqFt"].mean()) / opp_df["ProfitPerSqFt"].std()
    sat_norm = (opp_df["CustomerSatisfaction"] - opp_df["CustomerSatisfaction"].mean()) / opp_df["CustomerSatisfaction"].std()

    # Higher score = better performance; opportunity could be seen as inverse,
    # but here we keep it as a performance score for ranking
    opportunity_score = (sales_sq_norm + profit_sq_norm + sat_norm) / 3.0

    print("\nTop 10 Store-Department Combinations by Profit:")
    print(top_combinations)
    print("\nBottom 10 Store-Department Combinations by Profit:")
    print(underperforming)
    print("\nStore Opportunity/Performance Score:")
    print(opportunity_score.sort_values(ascending=False))

    return {
        "top_combinations": top_combinations,
        "underperforming": underperforming,
        "opportunity_score": opportunity_score
    }

# 4.2 Develop recommendations for improving performance
# REQUIRED: Return list of recommendations
def develop_recommendations():
    """
    Develop actionable recommendations based on the analysis
    REQUIRED: Return list of at least 5 recommendation strings
    """
    sales_metrics = analyze_sales_performance()
    customer_analysis = analyze_customer_segments()
    store_comparison = compare_store_performance()
    opportunities = identify_profit_opportunities()

    top_store = sales_metrics["sales_by_store"].idxmax()
    top_dept = sales_metrics["sales_by_dept"].idxmax()
    highest_segment = customer_analysis["segment_avg_spend"].idxmax()
    weakest_store = store_comparison["performance_ranking"].idxmax()

    recommendations = [
        f"Replicate best practices from {top_store}, the highest-sales store, across lower-performing locations such as {weakest_store}.",
        f"Invest in expanding the {top_dept} department chain-wide, as it generates the highest total sales.",
        f"Design targeted marketing and loyalty campaigns for the '{highest_segment}' segment, which has the highest average monthly spend.",
        "Increase staffing and training during weekends, when sales volumes are significantly higher, to improve service and basket size.",
        "Allocate additional marketing budget and in-store promotions to store–department combinations in the underperforming group to lift profitability.",
    ]

    print("\nRecommendations:")
    for rec in recommendations:
        print(f"- {rec}")

    return recommendations


# TODO 5: Summary Report
# REQUIRED: Generate comprehensive summary
def generate_executive_summary():
    """
    Generate an executive summary of key findings and recommendations
    REQUIRED: Print executive summary with sections:
    - Overview (1 paragraph)
    - Key Findings (3-5 bullet points)
    - Recommendations (3-5 bullet points)
    - Expected Impact (1 paragraph)
    """
    sales_metrics = analyze_sales_performance()
    customer_analysis = analyze_customer_segments()
    correlations = analyze_sales_correlations()
    store_comparison = compare_store_performance()
    opportunities = identify_profit_opportunities()
    recommendations = develop_recommendations()

    total_sales = sales_metrics["total_sales"]
    total_profit = sales_metrics["total_profit"]
    avg_margin = sales_metrics["avg_profit_margin"]
    top_store = sales_metrics["sales_by_store"].idxmax()
    top_dept = sales_metrics["sales_by_dept"].idxmax()
    top_segment = customer_analysis["segment_avg_spend"].idxmax()

    print("\nEXECUTIVE SUMMARY")
    print("-" * 60)

    # Overview
    print("\nOverview:")
    print(
        f"GreenGrocer’s five Florida locations generated approximately ${total_sales:,.0f} in sales "
        f"and ${total_profit:,.0f} in profit over the past year, with an average profit margin of "
        f"{avg_margin:.1%}. This analysis integrates sales, customer, and operational data to "
        f"highlight performance drivers and identify opportunities for growth."
    )

    # Key Findings
    print("\nKey Findings:")
    print(f"- {top_store} is the strongest store by total sales, while some locations lag in profit performance.")
    print(f"- The {top_dept} department leads in sales contribution, indicating strong customer demand.")
    print(f"- The '{top_segment}' customer segment shows the highest average monthly spend.")
    print("- Weekend days consistently outperform weekdays in sales, confirming strong temporal seasonality.")
    print("- Store characteristics such as square footage, staffing, and marketing spend show measurable correlation with annual sales.")

    # Recommendations
    print("\nRecommendations:")
    for rec in recommendations[:5]:
        print(f"- {rec}")

    # Expected Impact
    print("\nExpected Impact:")
    print(
        "Implementing these recommendations is expected to lift overall revenue and profitability by focusing "
        "resources on high-performing stores, departments, and customer segments while systematically improving "
        "underperforming areas. Over the next year, GreenGrocer can expect more efficient use of marketing and "
        "operational budgets, stronger customer loyalty, and a more balanced performance profile across all stores.")