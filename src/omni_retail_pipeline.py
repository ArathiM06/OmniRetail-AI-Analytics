"""
OmniRetail AI: Intelligent Multi-Channel Customer Analytics & Churn Prediction System
AICTE | IBM SkillsBuild Data Analytics with AI Internship Program 2026
BharatCares - Final Capstone Implementation Pipeline
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix, classification_report
)

# Visual styling
sns.set_theme(style="whitegrid", font="sans-serif")
plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 14,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.titlesize": 16
})

os.makedirs("figures", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

def run_pipeline(data_path="data/omni_retail_transactions.csv"):
    print("=" * 75)
    print(" [STAGE 1] DATA INGESTION & DATA QUALITY VALIDATION")
    print("=" * 75)
    
    df = pd.read_csv(data_path)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    
    print(f"Total Transactions Loaded : {len(df):,}")
    print(f"Total Unique Customers    : {df['Customer_ID'].nunique():,}")
    print(f"Date Range                : {df['Order_Date'].min().strftime('%Y-%m-%d')} to {df['Order_Date'].max().strftime('%Y-%m-%d')}")
    print(f"Missing Values Check      : {df.isnull().sum().sum()} nulls found")
    print(f"Duplicate Rows Check      : {df.duplicated().sum()} duplicates found")
    
    # -------------------------------------------------------------
    # STAGE 2: EXPLORATORY DATA ANALYSIS (EDA) & BUSINESS METRICS
    # -------------------------------------------------------------
    print("\n" + "=" * 75)
    print(" [STAGE 2] EXPLORATORY DATA ANALYSIS & CORE BUSINESS METRICS")
    print("=" * 75)
    
    total_rev = df["Revenue"].sum()
    total_profit = df["Profit"].sum()
    avg_order_value = df["Revenue"].mean()
    avg_rating = df["Rating"].mean()
    margin_pct = (total_profit / total_rev) * 100
    
    print(f"Gross Platform Revenue    : INR {total_rev:,.2f}")
    print(f"Net Operating Profit      : INR {total_profit:,.2f} ({margin_pct:.1f}% margin)")
    print(f"Average Order Value (AOV) : INR {avg_order_value:,.2f}")
    print(f"Average Customer Rating   : {avg_rating:.2f} / 5.00")
    
    # 1. Monthly Revenue Trend
    df["YearMonth"] = df["Order_Date"].dt.to_period("M").astype(str)
    monthly_summary = df.groupby("YearMonth").agg(
        Monthly_Revenue=("Revenue", "sum"),
        Monthly_Profit=("Profit", "sum"),
        Order_Count=("Order_ID", "count")
    ).reset_index()
    
    fig, ax1 = plt.subplots(figsize=(11, 5))
    ax2 = ax1.twinx()
    
    bars = ax1.bar(monthly_summary["YearMonth"], monthly_summary["Monthly_Revenue"] / 1000, 
                   color="#1A73E8", alpha=0.85, width=0.55, label="Revenue (k INR)")
    lines = ax2.plot(monthly_summary["YearMonth"], monthly_summary["Monthly_Profit"] / 1000, 
                     color="#E37400", marker="o", linewidth=2.5, label="Profit (k INR)")
    
    ax1.set_xlabel("Month-Year", fontweight="bold")
    ax1.set_ylabel("Revenue (Thousands INR)", color="#1A73E8", fontweight="bold")
    ax2.set_ylabel("Profit (Thousands INR)", color="#E37400", fontweight="bold")
    ax1.set_xticklabels(monthly_summary["YearMonth"], rotation=45, ha="right")
    ax1.grid(axis="y", linestyle="--", alpha=0.6)
    ax2.grid(False)
    
    plt.title("OmniRetail Monthly Revenue & Net Profit Trajectory (2025-2026)", fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig("figures/01_monthly_revenue_trend.png", dpi=300)
    plt.close()
    print("Saved figure: figures/01_monthly_revenue_trend.png")
    
    # 2. Category Performance (Revenue & Profit)
    cat_summary = df.groupby("Category").agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Items_Sold=("Quantity", "sum")
    ).sort_values("Revenue", ascending=False).reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    y = np.arange(len(cat_summary))
    height = 0.35
    
    ax.barh(y - height/2, cat_summary["Revenue"] / 1000, height, label="Revenue (k INR)", color="#34A853")
    ax.barh(y + height/2, cat_summary["Profit"] / 1000, height, label="Profit (k INR)", color="#4285F4")
    
    ax.set_yticks(y)
    ax.set_yticklabels(cat_summary["Category"], fontweight="bold")
    ax.invert_yaxis()
    ax.set_xlabel("Amount (Thousands INR)", fontweight="bold")
    ax.set_title("Product Category Performance: Revenue vs. Profit Contribution", fontweight="bold", pad=15)
    ax.legend(frameon=True)
    plt.tight_layout()
    plt.savefig("figures/02_category_performance.png", dpi=300)
    plt.close()
    print("Saved figure: figures/02_category_performance.png")
    
    # 3. Branch Performance
    branch_summary = df.groupby(["Branch", "City"]).agg(
        Branch_Revenue=("Revenue", "sum"),
        Branch_Profit=("Profit", "sum"),
        Orders=("Order_ID", "count"),
        Avg_Rating=("Rating", "mean")
    ).sort_values("Branch_Revenue", ascending=False).reset_index()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    colors = ["#4285F4", "#EA4335", "#FBBC05", "#34A853"]
    
    ax1.pie(branch_summary["Branch_Revenue"], labels=branch_summary["City"], autopct="%1.1f%%",
            startangle=140, colors=colors, wedgeprops=dict(width=0.45, edgecolor='w', linewidth=2))
    ax1.set_title("Revenue Share by Metro Branch", fontweight="bold")
    
    sns.barplot(data=branch_summary, x="City", y="Avg_Rating", palette=colors, ax=ax2, hue="City", legend=False)
    ax2.set_ylim(0, 5)
    ax2.set_title("Customer Satisfaction (CSAT) by Branch", fontweight="bold")
    ax2.set_ylabel("Average Rating (1-5)")
    for p in ax2.patches:
        ax2.annotate(f"{p.get_height():.2f}", (p.get_x() + p.get_width() / 2., p.get_height() - 0.4),
                     ha="center", color="white", fontweight="bold")
        
    plt.tight_layout()
    plt.savefig("figures/03_branch_performance.png", dpi=300)
    plt.close()
    print("Saved figure: figures/03_branch_performance.png")
    
    # 4. Payment Modes and Membership Comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    pay_counts = df["Payment_Method"].value_counts()
    sns.barplot(x=pay_counts.values, y=pay_counts.index, palette="Blues_r", ax=ax1, hue=pay_counts.index, legend=False)
    ax1.set_title("Transaction Volume by Payment Gateway", fontweight="bold")
    ax1.set_xlabel("Number of Transactions")
    
    cust_agg = df.groupby("Customer_Type").agg(
        AOV=("Revenue", "mean"),
        Avg_Rating=("Rating", "mean"),
        Total_Rev=("Revenue", "sum")
    ).reset_index()
    
    sns.barplot(data=cust_agg, x="Customer_Type", y="AOV", palette=["#9C27B0", "#00BCD4"], ax=ax2, hue="Customer_Type", legend=False)
    ax2.set_title("Average Order Value: Members vs. Normal Customers", fontweight="bold")
    ax2.set_ylabel("Average Order Value (INR)")
    for p in ax2.patches:
        ax2.annotate(f"INR {p.get_height():,.0f}", (p.get_x() + p.get_width() / 2., p.get_height() / 2),
                     ha="center", color="white", fontweight="bold")
                     
    plt.tight_layout()
    plt.savefig("figures/04_payment_and_customer_segments.png", dpi=300)
    plt.close()
    print("Saved figure: figures/04_payment_and_customer_segments.png")
    
    # -------------------------------------------------------------
    # STAGE 3: CUSTOMER INTELLIGENCE & RFM SEGMENTATION
    # -------------------------------------------------------------
    print("\n" + "=" * 75)
    print(" [STAGE 3] CUSTOMER INTELLIGENCE: RFM SEGMENTATION")
    print("=" * 75)
    
    snapshot_date = df["Order_Date"].max() + pd.Timedelta(days=1)
    
    rfm = df.groupby("Customer_ID").agg(
        Recency=("Order_Date", lambda x: (snapshot_date - x.max()).days),
        Frequency=("Order_ID", "count"),
        Monetary=("Revenue", "sum"),
        Avg_Rating=("Rating", "mean"),
        First_Purchase=("Order_Date", "min"),
        Last_Purchase=("Order_Date", "max"),
        Customer_Type=("Customer_Type", "first")
    ).reset_index()
    
    rfm["AOV"] = rfm["Monetary"] / rfm["Frequency"]
    rfm["Tenure_Days"] = (snapshot_date - rfm["First_Purchase"]).dt.days
    
    # RFM Scoring using quantiles
    rfm["R_Score"] = pd.qcut(rfm["Recency"], 4, labels=[4, 3, 2, 1]).astype(int)
    rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
    rfm["M_Score"] = pd.qcut(rfm["Monetary"], 4, labels=[1, 2, 3, 4]).astype(int)
    rfm["RFM_Composite"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str) + rfm["M_Score"].astype(str)
    
    # Segment definition
    def segment_customer(row):
        r, f, m = row["R_Score"], row["F_Score"], row["M_Score"]
        if r >= 3 and f >= 3 and m >= 3:
            return "Champions (High Value, High Loyalty)"
        elif r >= 3 and f >= 2:
            return "Loyal Customers (Active Repeaters)"
        elif r >= 3 and f == 1:
            return "Promising Newcomers (Recent First Purchases)"
        elif r <= 2 and (f >= 3 or m >= 3):
            return "At Risk (Valuable Customers Disengaging)"
        else:
            return "Dormant / Churned (Inactive Low Value)"
            
    rfm["Customer_Segment"] = rfm.apply(segment_customer, axis=1)
    segment_counts = rfm["Customer_Segment"].value_counts().reset_index()
    segment_counts.columns = ["Segment", "Customer_Count"]
    
    print("Customer Segmentation Breakdown:")
    for _, r in segment_counts.iterrows():
        print(f"  * {r['Segment']:<42}: {r['Customer_Count']} accounts ({r['Customer_Count']/len(rfm)*100:.1f}%)")
        
    plt.figure(figsize=(10, 5))
    palette_rfm = ["#1B5E20", "#388E3C", "#FBC02D", "#F57C00", "#D32F2F"]
    sns.countplot(data=rfm, y="Customer_Segment", order=rfm["Customer_Segment"].value_counts().index, palette=palette_rfm, hue="Customer_Segment", legend=False)
    plt.title("Distribution of Customer RFM Strategic Segments", fontweight="bold", pad=15)
    plt.xlabel("Number of Customers")
    plt.ylabel("Segment Category")
    plt.tight_layout()
    plt.savefig("figures/05_rfm_customer_segments.png", dpi=300)
    plt.close()
    print("Saved figure: figures/05_rfm_customer_segments.png")
    
    # -------------------------------------------------------------
    # STAGE 4: LEAKAGE-SAFE PREDICTIVE CHURN MODELING
    # -------------------------------------------------------------
    print("\n" + "=" * 75)
    print(" [STAGE 4] LEAKAGE-SAFE PREDICTIVE MACHINE LEARNING MODELING")
    print("=" * 75)
    
    # Strictly split timeline to prevent target leakage (Masterclass 3 pedagogy):
    # Historical Observation Window: First 280 days (Jan 1, 2025 to Oct 7, 2025)
    # Outcome / Future Prediction Window: Post day 280 (Oct 8, 2025 to end)
    cutoff_date = df["Order_Date"].min() + pd.Timedelta(days=280)
    print(f"Historical Cutoff Date    : {cutoff_date.strftime('%Y-%m-%d')}")
    
    hist_df = df[df["Order_Date"] <= cutoff_date]
    future_df = df[df["Order_Date"] > cutoff_date]
    
    active_customers = hist_df["Customer_ID"].unique()
    future_active_customers = set(future_df["Customer_ID"].unique())
    
    ml_records = []
    for cid in active_customers:
        c_hist = hist_df[hist_df["Customer_ID"] == cid]
        recency_hist = (cutoff_date - c_hist["Order_Date"].max()).days
        frequency_hist = len(c_hist)
        monetary_hist = c_hist["Revenue"].sum()
        aov_hist = monetary_hist / frequency_hist
        avg_rating_hist = c_hist["Rating"].mean()
        is_member = 1 if c_hist["Customer_Type"].iloc[0] == "Member" else 0
        tenure_hist = (cutoff_date - c_hist["Order_Date"].min()).days
        
        # Ground Truth Label: 1 if customer did NOT purchase in the future window (Churned), 0 if active
        churn_label = 0 if cid in future_active_customers else 1
        
        ml_records.append({
            "Customer_ID": cid,
            "Recency": recency_hist,
            "Frequency": frequency_hist,
            "Monetary": monetary_hist,
            "AOV": aov_hist,
            "Avg_Rating": avg_rating_hist,
            "Is_Member": is_member,
            "Tenure_Days": tenure_hist,
            "Churn": churn_label
        })
        
    ml_df = pd.DataFrame(ml_records)
    print(f"Historical Customer Cohort Size: {len(ml_df)}")
    print(f"Churn Label Distribution       :\n{ml_df['Churn'].value_counts(normalize=True).round(3)}")
    
    feature_cols = ["Recency", "Frequency", "Monetary", "AOV", "Avg_Rating", "Is_Member", "Tenure_Days"]
    X = ml_df[feature_cols]
    y = ml_df["Churn"]
    
    X_train, X_test, y_train, y_test, id_train, id_test = train_test_split(
        X, y, ml_df["Customer_ID"], test_size=0.25, random_state=42, stratify=y
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Models to benchmark
    models = {
        "Logistic Regression": LogisticRegression(random_state=42, max_iter=1000),
        "Decision Tree": DecisionTreeClassifier(random_state=42, max_depth=4),
        "Random Forest": RandomForestClassifier(random_state=42, n_estimators=100, max_depth=5)
    }
    
    results = {}
    preds = {}
    probs = {}
    
    print("\nModel Benchmark Performance on Test Set:")
    print("-" * 75)
    print(f"{'Model':<22} | {'Accuracy':<9} | {'Precision':<9} | {'Recall':<9} | {'F1-Score':<9} | {'ROC-AUC':<9}")
    print("-" * 75)
    
    for name, model in models.items():
        if name == "Logistic Regression":
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            y_prob = model.predict_proba(X_test_scaled)[:, 1]
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1]
            
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        auc = roc_auc_score(y_test, y_prob)
        
        results[name] = {"Accuracy": acc, "Precision": prec, "Recall": rec, "F1-Score": f1, "ROC-AUC": auc}
        preds[name] = y_pred
        probs[name] = y_prob
        
        print(f"{name:<22} | {acc:.4f}    | {prec:.4f}    | {rec:.4f}    | {f1:.4f}    | {auc:.4f}")
    print("-" * 75)
    
    # 6. Confusion Matrices Comparison
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    for i, (name, y_pred) in enumerate(preds.items()):
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=axes[i],
                    xticklabels=["Retained (0)", "Churned (1)"], yticklabels=["Retained (0)", "Churned (1)"])
        axes[i].set_title(f"{name}\nConfusion Matrix", fontweight="bold")
        axes[i].set_xlabel("Predicted Label")
        axes[i].set_ylabel("Actual Label")
    plt.tight_layout()
    plt.savefig("figures/06_confusion_matrices.png", dpi=300)
    plt.close()
    print("Saved figure: figures/06_confusion_matrices.png")
    
    # 7. ROC Curves
    plt.figure(figsize=(8, 6))
    for name, y_prob in probs.items():
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        plt.plot(fpr, tpr, label=f"{name} (AUC = {results[name]['ROC-AUC']:.3f})", linewidth=2)
    plt.plot([0, 1], [0, 1], "k--", alpha=0.6, label="Random Chance (0.50)")
    plt.title("ROC Curves Comparison for Customer Churn Prediction", fontweight="bold", pad=15)
    plt.xlabel("False Positive Rate (1 - Specificity)")
    plt.ylabel("True Positive Rate (Recall)")
    plt.legend(frameon=True, loc="lower right")
    plt.tight_layout()
    plt.savefig("figures/07_roc_curves.png", dpi=300)
    plt.close()
    print("Saved figure: figures/07_roc_curves.png")
    
    # 8. Feature Importance
    rf_model = models["Random Forest"]
    rf_feat_imp = pd.Series(rf_model.feature_importances_, index=feature_cols).sort_values(ascending=True)
    
    plt.figure(figsize=(9, 5))
    rf_feat_imp.plot(kind="barh", color="#1A73E8")
    plt.title("Random Forest Gini Feature Importance for Churn Prediction", fontweight="bold", pad=15)
    plt.xlabel("Importance Score")
    plt.ylabel("Engineered Feature")
    plt.tight_layout()
    plt.savefig("figures/08_feature_importance.png", dpi=300)
    plt.close()
    print("Saved figure: figures/08_feature_importance.png")
    
    # 9. Output Table of Predictions
    test_results_df = pd.DataFrame({
        "Customer_ID": id_test,
        "Actual_Churn": y_test,
        "Predicted_Churn_LR": preds["Logistic Regression"],
        "Churn_Probability_LR": probs["Logistic Regression"].round(4),
        "Predicted_Churn_RF": preds["Random Forest"],
        "Churn_Probability_RF": probs["Random Forest"].round(4)
    }).reset_index(drop=True)
    
    # Attach customer value
    test_results_df = test_results_df.merge(
        ml_df[["Customer_ID", "Monetary", "Frequency", "Recency", "Is_Member"]], on="Customer_ID", how="left"
    )
    
    # Identify high priority retention targets (High risk probability + High monetary value)
    test_results_df["Retention_Priority"] = np.where(
        (test_results_df["Churn_Probability_RF"] >= 0.65) & (test_results_df["Monetary"] > test_results_df["Monetary"].median()),
        "HIGH PRIORITY (Tier 1)",
        np.where(test_results_df["Churn_Probability_RF"] >= 0.50, "MEDIUM PRIORITY (Tier 2)", "LOW RISK / STABLE")
    )
    
    test_results_df.to_csv("outputs/customer_churn_predictions.csv", index=False)
    print(f"Saved prediction results: outputs/customer_churn_predictions.csv ({len(test_results_df)} records)")
    
    # -------------------------------------------------------------
    # STAGE 5: IBM BOB STRATEGIC BUSINESS SOLUTIONS
    # -------------------------------------------------------------
    print("\n" + "=" * 75)
    print(" [STAGE 5] IBM BOB BUSINESS SOLUTION BLUEPRINT & ROI ANALYSIS")
    print("=" * 75)
    
    high_priority_cohort = test_results_df[test_results_df["Retention_Priority"] == "HIGH PRIORITY (Tier 1)"]
    at_risk_revenue = high_priority_cohort["Monetary"].sum()
    est_retention_rate = 0.35  # Industry standard win-back with targeted incentive
    protected_revenue = at_risk_revenue * est_retention_rate
    campaign_cost = len(high_priority_cohort) * 500  # INR 500 per customer incentive
    net_roi = ((protected_revenue - campaign_cost) / campaign_cost) * 100 if campaign_cost > 0 else 0
    
    print(f"High-Value At-Risk Customers Identified : {len(high_priority_cohort)}")
    print(f"Total Revenue Exposed to Churn Risk      : INR {at_risk_revenue:,.2f}")
    print(f"Projected Recovered Revenue (35% win-back): INR {protected_revenue:,.2f}")
    print(f"Retention Campaign Cost (Incentive spend): INR {campaign_cost:,.2f}")
    print(f"Expected Net ROI on AI Retention Campaign : {net_roi:,.1f}%")
    print("=" * 75)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    
    return {
        "monthly_summary": monthly_summary,
        "cat_summary": cat_summary,
        "branch_summary": branch_summary,
        "rfm_counts": segment_counts,
        "model_results": results,
        "rf_feat_imp": rf_feat_imp,
        "bob_metrics": {
            "total_rev": total_rev,
            "total_profit": total_profit,
            "avg_order_value": avg_order_value,
            "avg_rating": avg_rating,
            "at_risk_revenue": at_risk_revenue,
            "protected_revenue": protected_revenue,
            "net_roi": net_roi,
            "high_priority_count": len(high_priority_cohort)
        }
    }

if __name__ == "__main__":
    run_pipeline()
