# e-commerce-sales-dashboard
# 🛒 E-Commerce Sales Performance Dashboard

**Tools:** Python · Pandas · NumPy · Matplotlib · Seaborn · Power BI · SQL  
**Domain:** Retail Analytics · Business Intelligence  
**Status:** Completed

---

## 📌 Project Overview

Analyzed over **50,000 transaction records** from an e-commerce platform to identify sales trends, top-performing product categories, and customer segments. Built an interactive Power BI dashboard for stakeholder reporting and automated the data preparation pipeline using Python.

---

## 🎯 Objectives

- Identify revenue trends over time (daily, monthly, quarterly)
- Determine top-performing product categories and regions
- Segment customers by purchase behaviour and lifetime value
- Automate data cleaning to reduce manual preparation effort
- Deliver an interactive dashboard for business stakeholders

---

## 📊 Key Results

| Metric | Result |
|---|---|
| Records analyzed | 50,000+ transactions |
| Data prep time reduction | ~60% via automated pipeline |
| Dashboard KPIs | Revenue, Conversion Rate, AOV, Regional Performance |
| Customer segments identified | 4 distinct behavioural segments |

---

## 🗂️ Project Structure

```
ecommerce-sales-dashboard/
│
├── data/
│   ├── raw/                  # Raw CSV data (sample)
│   └── cleaned/              # Processed data output
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_exploratory_analysis.ipynb
│   ├── 03_customer_segmentation.ipynb
│   └── 04_cohort_analysis.ipynb
│
├── sql/
│   └── sales_queries.sql     # SQL queries for aggregation & reporting
│
├── dashboard/
│   └── sales_dashboard.pbix  # Power BI dashboard file
│
├── outputs/
│   └── figures/              # Exported charts and visuals
│
├── requirements.txt
└── README.md
```

---

## 🔍 Approach

### 1. Data Cleaning & Preparation
- Handled missing values, duplicate records, and data type inconsistencies
- Standardized date formats and currency fields
- Automated the full pipeline using Python — reduced manual prep time by 60%

### 2. Exploratory Data Analysis (EDA)
- Analyzed revenue trends by day, month, and quarter
- Identified top 10 product categories by revenue and order volume
- Visualized regional performance using bar charts and heatmaps

### 3. Customer Segmentation
- Applied RFM analysis (Recency, Frequency, Monetary) to segment customers
- Identified 4 distinct segments: Champions, Loyal, At-Risk, and Lost
- Visualized segment distribution using Seaborn

### 4. Cohort Analysis
- Tracked monthly customer retention by acquisition cohort
- Calculated Customer Lifetime Value (CLV) per cohort
- Surfaced insights on churn timing to support marketing decisions

### 5. Power BI Dashboard
- Built interactive dashboard with KPI cards, time-series charts, and regional maps
- Added slicers for date range, product category, and region
- Enabled drill-through pages for product-level and customer-level detail

---

## ⚙️ How to Run

1. **Clone the repository**
```bash
git clone https://github.com/madhuri-sandhi/ecommerce-sales-dashboard.git
cd ecommerce-sales-dashboard
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run notebooks in order**
```bash
jupyter notebook notebooks/
```

4. **Open the dashboard**  
Open `dashboard/sales_dashboard.pbix` in Power BI Desktop.

---

## 📦 Requirements

```
pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.6.0
seaborn>=0.12.0
scikit-learn>=1.1.0
jupyter>=1.0.0
openpyxl>=3.0.0
```

---

## 💡 Key Learnings

- Automating repetitive data cleaning steps dramatically reduces analysis turnaround time
- RFM segmentation is a practical, interpretable method for customer prioritization
- Power BI slicers and drill-throughs significantly improve stakeholder engagement vs. static reports
