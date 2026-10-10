# 🛍️ OmniRetail AI: Intelligent Multi-Channel Customer Analytics, RFM Intelligence & Predictive Churn System

[![AICTE Internship](https://img.shields.io/badge/AICTE-Internship%202026-blue.svg)](https://internship.aicte-india.org/)
[![IBM SkillsBuild](https://img.shields.io/badge/IBM%20SkillsBuild-Certified-052FAD.svg)](https://skills.yourlearning.ibm.com/)
[![BharatCares](https://img.shields.io/badge/Partner-BharatCares-green.svg)](https://bharatcares.org/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Final Capstone Submission for Certificate Verification**  
> **Program:** AICTE | IBM SkillsBuild Data Analytics with AI Internship Program 2026  
> **Implementing Partner:** BharatCares  
> **Program Lead / Trainer:** Mr. Kartik Hooda  
> **Intern:** Arathi M (`itsarathi006@gmail.com`)

---

## 📖 Table of Contents
- [Executive Overview](#-executive-overview)
- [Internship Alignment & Learning Modules](#-internship-alignment--learning-modules)
- [Project Architecture & Methodology](#-project-architecture--methodology)
- [Dataset Overview & Data Dictionary](#-dataset-overview--data-dictionary)
- [Exploratory Data Analysis (EDA) Highlights](#-exploratory-data-analysis-eda-highlights)
- [Customer Intelligence: RFM Segmentation](#-customer-intelligence-rfm-segmentation)
- [Leakage-Safe Predictive Machine Learning](#-leakage-safe-predictive-machine-learning)
- [IBM BOB Business Opportunity Blueprint & ROI](#-ibm-bob-business-opportunity-blueprint--roi)
- [Project Directory Structure](#-project-directory-structure)
- [Installation & Quickstart Guide](#-installation--quickstart-guide)
- [Submission Deliverables Checklist](#-submission-deliverables-checklist)

---

## 🎯 Executive Overview
OmniRetail AI is an enterprise-scale analytical and predictive machine learning system developed to solve one of the most critical challenges in modern omnichannel commerce: **silent customer churn**. 

While acquiring a new retail customer costs **5x to 7x more** than retaining an existing customer, retail operations frequently lose high-value accounts without early warning. By combining multi-channel sales telemetry across four Indian metropolitan branches (Mumbai, Bangalore, Delhi, Hyderabad), OmniRetail AI:
1. Conducts granular **descriptive and diagnostic analytics** on sales, margins, and customer satisfaction (CSAT).
2. Generates customer behavioral profiles using **Recency, Frequency, and Monetary (RFM) segmentation**.
3. Deploys a **leakage-safe predictive machine learning architecture** to forecast churn risk 90–180 days in advance.
4. Translates analytical risk scores into an **IBM BOB (Business Opportunity Blueprint) action plan** with a projected **4,356% net ROI** on retention campaigns.

---

## 📚 Internship Alignment & Learning Modules
This capstone directly integrates every concept and workbook from the **AICTE | IBM SkillsBuild Masterclass Series**:

| Masterclass | Topic | Implemented In OmniRetail AI |
| :--- | :--- | :--- |
| **MC 1** | **Data Fundamentals** | Tabular data modeling, relational keys, gross/net revenue formulas, order attributes. |
| **MC 2** | **Data Cleaning & Preparation** | Handling nulls, duplicate deduplication, ISO datetime parsing, monthly sales trends, multi-category profitability. |
| **MC 3** | **AI for Data Analytics** | Customer-level aggregation, RFM features, **leakage-safe temporal cutoff**, logistic regression & random forest churn models. |
| **MC 4** | **Business Solutions with IBM BOB** | Supermarket multi-branch diagnostic framework, identifying root causes, financial win-back models, actionable business decisions. |

---

## 🏗️ Project Architecture & Methodology

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                             OmniRetail AI Pipeline                           │
└──────────────────────────────────────┬───────────────────────────────────────┘
                                       │
     ┌─────────────────────────────────┴─────────────────────────────────┐
     ▼                                                                   ▼
[Stage 1: Ingestion & Hygiene]                               [Stage 2: Exploratory Analytics]
- 1,800 Transactions across 4 Metros                          - Monthly revenue & margin trends
- Schema validation, 0 nulls, 0 duplicates                    - Product category profitability
- Chronological sorting & ISO dates                           - Branch performance & CSAT (1-5)
     │                                                                   │
     └─────────────────────────────────┬─────────────────────────────────┘
                                       │
                                       ▼
                     [Stage 3: Customer RFM Segmentation]
                     - Recency (R), Frequency (F), Monetary (M), AOV
                     - Quintile scoring (1-4)
                     - Segment mapping: Champions, Loyal, At-Risk, etc.
                                       │
                                       ▼
              [Stage 4: Leakage-Safe Predictive Machine Learning]
              - Strict Historical Cutoff (Day 1 - 280) vs. Future Window (Day 281+)
              - Features calculated purely from past behavior
              - Models: Logistic Regression, Decision Tree, Random Forest
              - Metrics: Accuracy, Precision, Recall, F1, ROC-AUC
                                       │
                                       ▼
                 [Stage 5: IBM BOB Strategic Business Action]
                 - Identify Tier 1 High-Risk, High-Monetary Customers
                 - Targeted VIP retention incentives (INR 500 voucher)
                 - Financial ROI quantification (4,356% Net ROI)
```

---

## 📊 Dataset Overview & Data Dictionary
The underlying dataset is located at [`data/omni_retail_transactions.csv`](data/omni_retail_transactions.csv). It contains **1,800 transaction records** across **346 distinct customers** over a 15-month operational window.

### Data Dictionary
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `Order_ID` | String | Unique transaction reference code (e.g., `ORD10001`) |
| `Order_Date` | Datetime | Date of order execution (`YYYY-MM-DD`) |
| `Customer_ID` | String | Unique customer identifier (`CUST0001` - `CUST0350`) |
| `Customer_Type` | String | Membership tier: `Member` vs. `Normal` |
| `Branch` | String | Store designation: Branch A (Mumbai), Branch B (Bangalore), Branch C (Delhi), Branch D (Hyderabad) |
| `City` | String | Metropolitan city location |
| `Product` | String | Item SKU name (22 products across 6 categories) |
| `Category` | String | Product category: Electronics, Beverages, Fashion, Groceries, Home & Kitchen, Beauty |
| `Unit_Price` | Float | Item base price in INR |
| `Quantity` | Integer | Units purchased in order (1 - 6) |
| `Discount_Pct`| Float | Promotional discount fraction applied (0.00 - 0.20) |
| `Revenue` | Float | Realized gross transaction revenue (INR) |
| `Profit` | Float | Net operating profit contribution (INR) |
| `Payment_Method`| String | Payment mode: `UPI`, `Credit Card`, `Debit Card`, `Net Banking`, `Cash` |
| `Rating` | Integer | Post-purchase feedback rating (1 to 5 stars) |

---

## 📈 Exploratory Data Analysis (EDA) Highlights

- **Overall Financial Performance:** Gross platform turnover of **INR 13,651,971.08** with an operating profit of **INR 3,489,754.97** (**25.6% net margin**).
- **Average Order Value (AOV):** **INR 7,584.43** across all transactions.
- **Top Product Categories:** Electronics generated the largest aggregate revenue (**INR 5.8M**), while Beverages and Beauty products achieved the highest percentage margins (**42% - 50%**).
- **Branch Leadership:** Branch C (Delhi) and Branch A (Mumbai) collectively contributed **over 55%** of all sales.
- **Customer Satisfaction:** Platform-wide CSAT averaged **3.89 / 5.00**, with Members reporting higher satisfaction (**4.25**) than non-members (**3.60**).
- **Payment Trends:** **UPI** was the most popular channel (**42.1%**), followed by Credit Cards (**27.8%**).

All generated figures are stored in the [`figures/`](figures/) directory:
- `figures/01_monthly_revenue_trend.png`
- `figures/02_category_performance.png`
- `figures/03_branch_performance.png`
- `figures/04_payment_and_customer_segments.png`

---

## 👥 Customer Intelligence: RFM Segmentation

Using the Masterclass 3 methodology, customer records were transformed into four core dimensions:
$$\text{Recency (R)} = \text{Snapshot Date} - \text{Last Order Date}$$
$$\text{Frequency (F)} = \text{Total Completed Orders}$$
$$\text{Monetary (M)} = \sum \text{Revenue}$$
$$\text{AOV} = \frac{\text{Monetary}}{\text{Frequency}}$$

### Strategic Cohorts Identified:
1. **Champions (21.4% / 74 accounts):** High recency, high frequency, high spend. Prime candidates for exclusive loyalty perks.
2. **Loyal Customers (20.2% / 70 accounts):** Regular buyers with consistent order habits.
3. **Promising Newcomers (8.4% / 29 accounts):** Recent first-time purchasers with high potential for onboarding nurture campaigns.
4. **At-Risk Customers (27.2% / 94 accounts):** Previously frequent purchasers whose intervals between orders have lengthened drastically.
5. **Dormant / Churned (22.8% / 79 accounts):** Low-frequency historical buyers who have ceased purchasing.

*Visualized in [`figures/05_rfm_customer_segments.png`](figures/05_rfm_customer_segments.png).*

---

## 🤖 Leakage-Safe Predictive Machine Learning

### ⚠️ Preventing Target Leakage (Masterclass 3 Core Rule)
In naive churn models, computing churn directly from recency within the same period gives the model the answer in advance. To eliminate lookahead bias:
- **Observation Window (Days 1 to 280):** Historical features ($X$) are computed exclusively from orders occurring on or before the cutoff date.
- **Outcome Window (Days 281+):** The target variable ($y$) is defined as `1` if the customer made zero purchases in the outcome window, and `0` otherwise.

### Model Benchmark Evaluation (Holdout Test Cohort)
| Machine Learning Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (Baseline)** | 68.97% | 75.00% | 76.36% | 0.7568 | **0.7795** |
| **Decision Tree Classifier** | 65.52% | 73.58% | 70.91% | 0.7222 | 0.6909 |
| **Random Forest Classifier (Champion)** | **68.97%** | **72.58%** | **81.82%** | **0.7692** | **0.7733** |

> **Key Analytical Takeaway:** For customer retention, **Recall is the critical metric** because failing to catch a churner (False Negative) leads directly to lost revenue. **Random Forest achieved 81.82% Recall**, successfully identifying 45 out of 55 churners.

Diagnostic visualizations:
- Confusion Matrices: [`figures/06_confusion_matrices.png`](figures/06_confusion_matrices.png)
- ROC Curves: [`figures/07_roc_curves.png`](figures/07_roc_curves.png)
- Gini Feature Importance: [`figures/08_feature_importance.png`](figures/08_feature_importance.png)

---

## 💼 IBM BOB Business Opportunity Blueprint & ROI

Applying the **Masterclass 4 IBM BOB framework**, analytical probabilities were translated into financial retention decisions:

| Metric | Business Value | Explanation |
| :--- | :--- | :--- |
| **Identified High-Value At-Risk Cohort** | **30 Accounts** | Customers with Churn Probability $\ge 0.65$ & spend above median. |
| **Gross Revenue at Risk** | **INR 1,909,687.08** | Historical spend exposed to potential attrition. |
| **Projected Recovered Revenue** | **INR 668,390.48** | Expected win-back rate of 35% with targeted intervention. |
| **Retention Campaign Budget** | **INR 15,000.00** | INR 500 VIP reactivation voucher per targeted account. |
| **Expected Net Campaign ROI** | **4,355.9%** | $\frac{\text{Recovered Revenue} - \text{Campaign Cost}}{\text{Campaign Cost}} \times 100$ |

---

## 📁 Project Directory Structure

```
├── ArathiM_OmniRetail_AI_Analytics.ipynb   # Complete executed Jupyter Notebook (Ready for submission)
├── ArathiM_OmniRetail_ProjectReport.docx    # Formatted Word Project Report with embedded plots
├── requirements.txt                        # Python dependencies
├── README.md                               # Project documentation & GitHub overview
├── data/
│   └── omni_retail_transactions.csv        # Comprehensive multi-channel transaction dataset
├── figures/
│   ├── 01_monthly_revenue_trend.png        # Monthly sales and profit trajectory
│   ├── 02_category_performance.png         # Category revenue vs. profit breakdown
│   ├── 03_branch_performance.png           # Metro branch share and CSAT comparison
│   ├── 04_payment_and_customer_segments.png# Payment mode and membership spend
│   ├── 05_rfm_customer_segments.png        # RFM customer segmentation distribution
│   ├── 06_confusion_matrices.png           # Benchmark confusion matrices
│   ├── 07_roc_curves.png                   # Model ROC curves
│   └── 08_feature_importance.png           # Feature importance ranking
├── outputs/
│   └── customer_churn_predictions.csv      # Customer-level prediction scoring & priority tiers
└── src/
    └── omni_retail_pipeline.py             # Modular end-to-end Python execution pipeline
```

---

## 🚀 Installation & Quickstart Guide

### 1. Clone or Download Repository
```bash
git clone https://github.com/<your-username>/OmniRetail-AI-Analytics.git
cd OmniRetail-AI-Analytics
```

### 2. Set Up Virtual Environment & Install Dependencies
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Run the Complete Analytics & Modeling Pipeline
```bash
python src/omni_retail_pipeline.py
```

### 4. Launch Jupyter Notebook
```bash
jupyter notebook ArathiM_OmniRetail_AI_Analytics.ipynb
```

---

## 📜 Acknowledgments
Sincere appreciation to:
- **AICTE (All India Council for Technical Education)** for spearheading national digital skill initiatives.
- **IBM SkillsBuild** for state-of-the-art educational tracks and cloud credentials.
- **BharatCares** for organizational coordination and internship execution.
- **Mr. Kartik Hooda**, Lead Mentor, for insightful masterclasses and hands-on guidance.
