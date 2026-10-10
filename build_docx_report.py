import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def create_report(author_name="Sarathi", filename="Sarathi_OmniRetail_ProjectReport.docx"):
    doc = Document()
    
    # Page Margins (1 inch all sides)
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        
    # Title / Cover Page Header
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_inst = p_inst.add_run("AICTE | IBM SkillsBuild | BharatCares\nData Analytics with AI Internship Program 2026")
    run_inst.font.name = "Arial"
    run_inst.font.size = Pt(13)
    run_inst.font.bold = True
    run_inst.font.color.rgb = RGBColor(0, 51, 102)
    
    doc.add_paragraph()
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("FINAL CAPSTONE PROJECT REPORT\n\nOmniRetail AI: Intelligent Multi-Channel Customer Analytics, RFM Intelligence & Predictive Churn System")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(20)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(26, 115, 232)
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("An End-to-End Implementation of Descriptive, Diagnostic, Predictive, and Prescriptive Analytics using the IBM Business Opportunity Blueprint (BOB)")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(12)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(100, 100, 100)
    
    doc.add_paragraph("\n" * 3)
    
    # Metadata Box Table
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Candidate Name", author_name),
        ("Internship Domain", "Data Analytics with AI: Foundation to Implementation"),
        ("Sponsoring Organizations", "AICTE, IBM SkillsBuild, BharatCares"),
        ("Program Lead / Trainer", "Mr. Kartik Hooda"),
        ("Submission Date", "October 2026")
    ]
    for i, (k, v) in enumerate(meta_data):
        row = meta_table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.5)
        c1.width = Inches(4.0)
        
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(k)
        r0.font.bold = True
        r0.font.size = Pt(10.5)
        
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(v)
        r1.font.size = Pt(10.5)
        
        set_cell_background(c0, "F0F4F8")
        set_cell_background(c1, "FFFFFF")
        
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # Executive Summary
    # -------------------------------------------------------------
    h_exec = doc.add_heading("Executive Summary", level=1)
    h_exec.style.font.color.rgb = RGBColor(0, 51, 102)
    
    p_exec = doc.add_paragraph(
        "Modern multi-channel retail organizations face fierce competitive pressures, fluctuating customer loyalty, "
        "and costly customer churn. This project, titled OmniRetail AI, presents an enterprise-grade analytics and "
        "predictive machine learning framework developed under the AICTE | IBM SkillsBuild Data Analytics with AI "
        "Internship Program 2026 in collaboration with BharatCares. Incorporating all core competencies from Masterclasses "
        "1 through 4 (Data Fundamentals, Data Cleaning, AI-powered Predictive Modeling, and IBM BOB Business Solution Framework), "
        "this solution synthesizes transactional data from four major Indian metropolitan branches to deliver actionable intelligence.\n\n"
        "Key Accomplishments & Findings:\n"
        "• Data Scale & Quality: Successfully ingested and cleaned 1,800 transaction records spanning 346 unique customer accounts across 15 months with zero missing values or data duplicates.\n"
        "• Financial & Operational Performance: Diagnosed INR 13.65 Million in gross platform revenue generating INR 3.49 Million net operating profit (25.6% profit margin). Branch C (Delhi) and Branch A (Mumbai) drove over 55% of total volume.\n"
        "• Customer RFM Segmentation: Segmented the customer base into 5 distinct behavioral tiers: Champions (21.4%), Loyal Customers (20.2%), Promising Newcomers (8.4%), At-Risk Accounts (27.2%), and Dormant Accounts (22.8%).\n"
        "• Leakage-Safe Machine Learning: Overcame the common industry pitfall of target leakage by establishing a strict temporal cutoff (Day 1-280 historical observation vs. Day 281+ outcome window). Benchmarked Logistic Regression, Decision Trees, and Random Forests, achieving 81.8% recall and 0.773 ROC-AUC on the test set.\n"
        "• IBM BOB Strategic Prescriptive ROI: Identified 30 top-tier at-risk customer accounts representing INR 1.91 Million in exposed revenue. A targeted proactive retention incentive campaign yields a projected net ROI of 4,356% with INR 668.4k in protected customer spend."
    )
    p_exec.style.font.size = Pt(11)
    
    # -------------------------------------------------------------
    # 1. Introduction & Background
    # -------------------------------------------------------------
    doc.add_heading("1. Introduction & Background", level=1)
    doc.add_paragraph(
        "Data analytics combined with Artificial Intelligence is fundamentally transforming modern retail. Retailers no longer rely on retrospective quarterly accounting; they leverage continuous behavioral telemetry to forecast inventory requirements, detect changing purchasing frequencies, and preempt customer attrition before accounts go cold.\n\n"
        "This project integrates the full pedagogy of the IBM SkillsBuild internship program:\n"
        "1. Masterclass 1: Data Fundamentals, understanding relational and tabular schemas, customer metrics, and business KPIs.\n"
        "2. Masterclass 2: Rigorous data cleaning, validation, datetime transformation, and visual exploratory analysis of sales and profitability trends.\n"
        "3. Masterclass 3: AI for Data Analytics, feature engineering of Recency, Frequency, and Monetary (RFM) variables, and training leakage-safe predictive classification algorithms.\n"
        "4. Masterclass 4: The IBM Business Opportunity Blueprint (BOB), converting data outputs into tangible operational decisions, capital allocation, and executive-level return on investment."
    )
    
    # -------------------------------------------------------------
    # 2. Problem Statement & Business Context
    # -------------------------------------------------------------
    doc.add_heading("2. Problem Statement & Business Context", level=1)
    doc.add_paragraph(
        "According to Bain & Company, acquiring a new retail customer costs 5 to 7 times more than retaining an existing customer, while increasing customer retention rates by just 5% can boost profits by 25% to 95%. Retailers frequently suffer from 'silent churn'—where previously regular shoppers gradually decrease order frequency and ultimately cease purchasing without ever lodging a formal complaint.\n\n"
        "The primary objectives of the OmniRetail AI initiative are:\n"
        "1. Unified Visibility: Provide unified visibility into store branches (Mumbai, Bangalore, Delhi, Hyderabad), product categories, and payment gateways.\n"
        "2. Customer Behavioral Segmentation: Systematically classify accounts by purchasing recency, visit frequency, and monetary contribution.\n"
        "3. Early Churn Warning System: Construct a predictive machine learning classifier to identify accounts with high probability of churning within the next 90-180 days.\n"
        "4. Actionable Retention Playbook: Design an automated, high-ROI intervention strategy based on the IBM BOB framework."
    )
    
    # -------------------------------------------------------------
    # 3. Dataset Description & Data Schema
    # -------------------------------------------------------------
    doc.add_heading("3. Dataset Description & Data Schema", level=1)
    doc.add_paragraph(
        "The project analyzes an omnichannel retail transaction repository containing 1,800 records across 346 individual customer accounts collected between January 2025 and March 2026. The data schema contains 15 granular attributes spanning customer profiles, geographic distribution, basket contents, financial metrics, and customer feedback."
    )
    
    # Schema Table
    schema_table = doc.add_table(rows=1, cols=4)
    schema_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Attribute Name", "Data Type", "Category", "Business Description"]
    hdr_cells = schema_table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        hdr_cells[i].paragraphs[0].runs[0].font.bold = True
        set_cell_background(hdr_cells[i], "1A73E8")
        hdr_cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        
    attributes = [
        ("Order_ID", "String (Categorical)", "Identifier", "Unique primary transaction key (e.g. ORD10001)"),
        ("Order_Date", "Datetime", "Temporal", "Timestamp of transaction execution"),
        ("Customer_ID", "String (Categorical)", "Identifier", "Unique customer identification code (CUST0001 - CUST0350)"),
        ("Customer_Type", "String (Categorical)", "Profile", "Membership tier ('Member' vs. 'Normal')"),
        ("Branch", "String (Categorical)", "Geography", "Store location ('Branch A', 'Branch B', 'Branch C', 'Branch D')"),
        ("City", "String (Categorical)", "Geography", "Metropolitan market (Mumbai, Bangalore, Delhi, Hyderabad)"),
        ("Product", "String (Categorical)", "Merchandise", "Specific SKU item description (22 distinct retail products)"),
        ("Category", "String (Categorical)", "Merchandise", "Product department (Electronics, Beverages, Fashion, Groceries, etc.)"),
        ("Unit_Price", "Float (Continuous)", "Financial", "Base selling price per item unit in INR"),
        ("Quantity", "Integer (Discrete)", "Basket", "Number of units purchased in transaction (1 - 6)"),
        ("Discount_Pct", "Float (Continuous)", "Financial", "Promotional markdown applied (0.00 to 0.20)"),
        ("Revenue", "Float (Continuous)", "Financial", "Gross realized revenue after discount in INR"),
        ("Profit", "Float (Continuous)", "Financial", "Net profit margin contribution in INR"),
        ("Payment_Method", "String (Categorical)", "Channel", "Gateway utilized (UPI, Credit Card, Debit Card, Net Banking, Cash)"),
        ("Rating", "Integer (Ordinal)", "Experience", "Post-purchase customer satisfaction score (1 to 5 stars)")
    ]
    
    for row_idx, item in enumerate(attributes):
        row = schema_table.add_row()
        for col_idx, text in enumerate(item):
            cell = row.cells[col_idx]
            cell.text = text
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)
            if row_idx % 2 == 1:
                set_cell_background(cell, "F7FAFC")
                
    # -------------------------------------------------------------
    # 4. Data Cleaning & Exploratory Data Analysis (EDA)
    # -------------------------------------------------------------
    doc.add_heading("4. Data Cleaning & Exploratory Data Analysis (EDA)", level=1)
    doc.add_paragraph(
        "Data preparation followed industry best practices: missing value verification confirmed 0 null entries; date strings were parsed into standard ISO-8601 timestamps; and data type casting was validated across numeric metrics. Summary statistics demonstrated an aggregate platform gross revenue of INR 13,651,971.08 with an overall operating profit of INR 3,489,754.97, yielding a healthy operating profit margin of 25.6%.\n\n"
        "Key Descriptive Insights:\n"
        "1. Trajectory Analysis: Revenue exhibited seasonal growth peaks with noticeable surges during festive promotional periods, accompanied by stable profit margins.\n"
        "2. Merchandise Contribution: Electronics generated the highest absolute revenue (INR 5.8M) due to high basket ticket sizes, while Beverages and Personal Care demonstrated the highest percentage margins (40%-50%).\n"
        "3. Regional Performance: Branch C (Delhi) and Branch A (Mumbai) contributed 28.5% and 31.8% of platform turnover respectively, while maintaining average CSAT ratings of 3.88 to 3.92 out of 5.\n"
        "4. Payment Channels & Memberships: UPI was the dominant payment mechanism, accounting for 42.1% of transactions, followed by Credit Cards (27.8%). Registered Members exhibited an Average Order Value of INR 8,120 compared to INR 7,140 for non-members."
    )
    
    if os.path.exists("figures/01_monthly_revenue_trend.png"):
        doc.add_paragraph("Figure 1: OmniRetail Monthly Revenue & Net Profit Trajectory (2025-2026)")
        doc.add_picture("figures/01_monthly_revenue_trend.png", width=Inches(6.0))
        
    if os.path.exists("figures/02_category_performance.png"):
        doc.add_paragraph("Figure 2: Merchandise Category Breakdown — Revenue vs. Net Operating Profit")
        doc.add_picture("figures/02_category_performance.png", width=Inches(6.0))
        
    if os.path.exists("figures/03_branch_performance.png"):
        doc.add_paragraph("Figure 3: Metro Branch Performance — Market Share and Customer Satisfaction (CSAT)")
        doc.add_picture("figures/03_branch_performance.png", width=Inches(6.0))
        
    if os.path.exists("figures/04_payment_and_customer_segments.png"):
        doc.add_paragraph("Figure 4: Payment Gateway Distribution and Member Spending Patterns")
        doc.add_picture("figures/04_payment_and_customer_segments.png", width=Inches(6.0))
        
    # -------------------------------------------------------------
    # 5. Customer Intelligence: RFM Segmentation
    # -------------------------------------------------------------
    doc.add_heading("5. Customer Intelligence: RFM Segmentation", level=1)
    doc.add_paragraph(
        "To transition from broad transaction-level analysis to customer-centric intelligence, we implemented the classic Recency-Frequency-Monetary (RFM) framework taught in Masterclass 3:\n"
        "• Recency (R): Days elapsed between the customer's most recent order and the observation snapshot date.\n"
        "• Frequency (F): Cumulative order count per customer.\n"
        "• Monetary (M): Cumulative gross revenue generated by the account.\n\n"
        "Each customer was assigned a quintile score from 1 to 4 across each dimension, yielding five business segments:\n"
        "1. Champions (21.4% / 74 accounts): High recency, high frequency, and high monetary spend. Our core advocates.\n"
        "2. Loyal Customers (20.2% / 70 accounts): Consistent repeat purchasers with moderate to high order volume.\n"
        "3. Promising Newcomers (8.4% / 29 accounts): Recent first-time purchasers exhibiting high potential for cross-selling.\n"
        "4. At-Risk Accounts (27.2% / 94 accounts): Previously valuable accounts whose purchase intervals have extended significantly.\n"
        "5. Dormant / Churned (22.8% / 79 accounts): Inactive accounts with minimal lifetime spend."
    )
    
    if os.path.exists("figures/05_rfm_customer_segments.png"):
        doc.add_paragraph("Figure 5: Strategic Customer Segmentation Breakdown")
        doc.add_picture("figures/05_rfm_customer_segments.png", width=Inches(6.0))
        
    # -------------------------------------------------------------
    # 6. Predictive Machine Learning Methodology
    # -------------------------------------------------------------
    doc.add_heading("6. Predictive Machine Learning Methodology", level=1)
    doc.add_paragraph(
        "A critical pitfall in customer churn modeling is Target Leakage (as highlighted in Masterclass 3, Part 6). When a model uses current recency to predict whether someone has purchased recently, it receives the answer in advance, yielding false 100% accuracy that collapses in production.\n\n"
        "Leakage-Safe Architecture Implementation:\n"
        "1. Temporal Split: We established a strict historical cutoff date (Day 280 / October 8, 2025). The period before Day 280 formed the Observation Window; the period after Day 280 formed the Outcome Window.\n"
        "2. Feature Engineering: For each customer active in the historical window, features (Historical Recency, Frequency, Monetary spend, AOV, CSAT, Member Flag, Tenure) were computed strictly from transactions occurring on or before Day 280.\n"
        "3. Ground-Truth Target Labeling: The binary target variable 'Churn' was assigned as 1 if the customer completed ZERO purchases in the subsequent outcome window, and 0 if they placed at least one subsequent order.\n"
        "4. Train/Test Partition: The 345 historical customer accounts were divided into 75% training and 25% holdout testing sets using stratified sampling to preserve class balance."
    )
    
    # -------------------------------------------------------------
    # 7. Model Evaluation & Comparative Performance
    # -------------------------------------------------------------
    doc.add_heading("7. Model Evaluation & Comparative Performance", level=1)
    doc.add_paragraph(
        "Three distinct classification algorithms were benchmarked on the identical test cohort: Logistic Regression, Decision Tree Classifier, and Random Forest Classifier."
    )
    
    # Benchmark Results Table
    bench_table = doc.add_table(rows=1, cols=6)
    bench_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    b_headers = ["Algorithm", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"]
    b_cells = bench_table.rows[0].cells
    for i, h in enumerate(b_headers):
        b_cells[i].text = h
        b_cells[i].paragraphs[0].runs[0].font.bold = True
        set_cell_background(b_cells[i], "1A73E8")
        b_cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        
    model_metrics = [
        ("Logistic Regression", "68.97%", "75.00%", "76.36%", "0.7568", "0.7795"),
        ("Decision Tree", "65.52%", "73.58%", "70.91%", "0.7222", "0.6909"),
        ("Random Forest (Champion)", "68.97%", "72.58%", "81.82%", "0.7692", "0.7733")
    ]
    for row_idx, item in enumerate(model_metrics):
        row = bench_table.add_row()
        for col_idx, text in enumerate(item):
            cell = row.cells[col_idx]
            cell.text = text
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)
            if row_idx % 2 == 1:
                set_cell_background(cell, "F7FAFC")
                
    doc.add_paragraph(
        "\nAnalysis of Results:\n"
        "In retention applications, Recall is the paramount metric because failing to identify an at-risk customer (False Negative) leads to permanent revenue forfeiture. The Random Forest Classifier achieved the highest Recall (81.82%) and F1-score (0.7692), correctly identifying 45 out of 55 churners in the test cohort while maintaining a robust ROC-AUC of 0.773."
    )
    
    if os.path.exists("figures/06_confusion_matrices.png"):
        doc.add_picture("figures/06_confusion_matrices.png", width=Inches(6.0))
        doc.add_paragraph("Figure 6: Confusion Matrix Comparison across Evaluated Classifiers")
        
    if os.path.exists("figures/07_roc_curves.png"):
        doc.add_picture("figures/07_roc_curves.png", width=Inches(5.5))
        doc.add_paragraph("Figure 7: Receiver Operating Characteristic (ROC) Benchmark Curves")
        
    if os.path.exists("figures/08_feature_importance.png"):
        doc.add_picture("figures/08_feature_importance.png", width=Inches(5.5))
        doc.add_paragraph("Figure 8: Random Forest Gini Feature Importance Breakdown")
        
    # -------------------------------------------------------------
    # 8. Business Solutions & Strategic Action Plan (IBM BOB)
    # -------------------------------------------------------------
    doc.add_heading("8. Business Solutions & Strategic Action Plan (IBM BOB)", level=1)
    doc.add_paragraph(
        "Applying the IBM Business Opportunity Blueprint (BOB) framework from Masterclass 4, analytical predictions were transformed into financial decisions and automated marketing workflows.\n\n"
        "1. Risk Prioritization Matrix:\n"
        "Each customer was assigned a Churn Probability score. Accounts with Churn Probability >= 0.65 AND historical monetary contribution above the median were categorized as Tier 1 HIGH PRIORITY.\n\n"
        "2. Financial Opportunity Quantification:\n"
        "• High-Value At-Risk Cohort: 30 critical accounts identified in test evaluation.\n"
        "• Exposed Revenue Volume: INR 1,909,687.08.\n"
        "• Projected Win-Back Rate: 35% with targeted intervention (conservative retail benchmark).\n"
        "• Recoverable Revenue: INR 668,390.48.\n"
        "• Retention Campaign Budget: INR 500 per customer incentive coupon = INR 15,000.00 total spend.\n"
        "• Net Projected ROI: ((INR 668,390.48 - INR 15,000.00) / INR 15,000.00) * 100 = 4,355.9% Net ROI."
    )
    
    # -------------------------------------------------------------
    # 9. Conclusion & Implementation Roadmap
    # -------------------------------------------------------------
    doc.add_heading("9. Conclusion & Implementation Roadmap", level=1)
    doc.add_paragraph(
        "The OmniRetail AI project confirms that integrating classical descriptive business intelligence with predictive machine learning provides a decisive competitive advantage in retail operations.\n\n"
        "Recommended 90-Day Implementation Roadmap:\n"
        "• Phase 1 (Weeks 1-3): Integrate the scoring pipeline with daily transactional databases. Automate feature computation for all active accounts.\n"
        "• Phase 2 (Weeks 4-6): Deploy automated triggers for Tier 1 high-risk customers, issuing personalized VIP re-engagement vouchers via SMS and WhatsApp integrated with UPI payment links.\n"
        "• Phase 3 (Weeks 7-12): Implement A/B testing across regional branches (Mumbai, Bangalore, Delhi, Hyderabad) to optimize incentive coupon denominations against actual customer lifetime value (CLV)."
    )
    
    # -------------------------------------------------------------
    # 10. References & Acknowledgments
    # -------------------------------------------------------------
    doc.add_heading("10. References & Acknowledgments", level=1)
    doc.add_paragraph(
        "This project was developed as part of the AICTE | IBM SkillsBuild Data Analytics with AI Internship Program 2026. Special gratitude is extended to:\n"
        "• All India Council for Technical Education (AICTE)\n"
        "• IBM SkillsBuild Academic Initiative\n"
        "• BharatCares Social Impact Foundation\n"
        "• Mr. Kartik Hooda, Lead Trainer & Industry Mentor, for foundational masterclass lectures, guidance on target leakage prevention, and the IBM BOB business solution framework."
    )
    
    doc.save(filename)
    print(f"[OK] Generated project report: {filename}")

if __name__ == "__main__":
    create_report("Sarathi", "Sarathi_OmniRetail_ProjectReport.docx")
    create_report("YourName", "YourName_OmniRetail_ProjectReport.docx")
