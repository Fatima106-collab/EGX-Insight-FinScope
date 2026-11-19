# EGX Insight – FinScope (End-to-End Financial & Stock Market Analysis)

An end-to-end automated data engineering, analytics, and business intelligence solution for analyzing financial statements and stock performance across **211 companies listed on the Egyptian Exchange (EGX)**[cite: 9].

---

## Project Pipeline & Architecture

### 1. Automated Web Scraping & ETL (`1_Python_Scraper`)
- **Automated Data Extraction:** Built a Python ETL script (`stock_analysis_scraper.py`) using `requests`, `pandas`, and `SQLAlchemy` to scrape **633 financial statement pages** (Income Statement, Balance Sheet, and Cash Flow Statement) across 211 EGX-listed companies[cite: 9, 103].
- **Data Cleaning & Transformation:** Standardized multi-index HTML tables, removed duplicate headers/rows, preserved line-item hierarchy (`Line_Order`), and reshaped wide financial tables into a normalized long format using `melt()`[cite: 9, 103].
- **Database Loading:** Automated direct ingestion into SQL Server (`Staging_Financials` table) via `pyodbc` with rate-limiting (`time.sleep`) and error handling (`try/except`)[cite: 9, 103].

### 2. Data Warehousing & SQL Analytics (`2_SQL_Query`)
- Designed relational staging and analytical tables in SQL Server.
- Wrote advanced SQL queries (CTEs, Window Functions, Views) to calculate financial ratios, YoY/QoQ growth, and sector-level benchmarks.

### 3. Interactive Power BI Dashboards (`PBI Files`)
Built a 5-page executive Power BI report with dynamic Company, Date, and Period (Yearly/Quarterly) slicers:

#### Page 1: Financial Performance Overview
Tracks core KPIs (Revenue, EBITDA, Net Income, Operating & Free Cash Flow, ROE), margin evolution, cash vs. net debt, and cash generation trends[cite: 104].
![Financial Performance Overview](Screen%20Shots/1.png)

#### Page 2: P&L & Cost Structure Analysis
Provides a detailed Profit & Loss statement matrix, YoY/QoQ revenue and cost growth cards, a P&L Waterfall bridge from Revenue to Net Income, and profitability breakdown[cite: 105].
![P&L and Cost Structure Analysis](Screen%20Shots/2.png)

#### Page 3: Financial Position & Capital Structure
Visualizes Assets, Liabilities, and Shareholders' Equity composition and historical mix alongside leverage metrics (Debt-to-Equity, Debt-to-Assets, Net Debt/EBITDA)[cite: 106].
![Financial Position and Capital Structure](Screen%20Shots/3.png)

#### Page 4: Liquidity, Solvency & Financial Leverage
Monitors Current, Quick, and Cash ratios, Working Capital, Interest Coverage, Debt Capacity (EBITDA vs. Interest Expense), and debt maturity trends[cite: 107].
![Liquidity, Solvency and Financial Leverage](Screen%20Shots/4.png)

#### Page 5: Working Capital & Asset Utilization
Analyzes Net Working Capital components (AR, Inventory, AP), Cash Conversion Cycle (DSO, DIO, DPO), and asset turnover efficiency[cite: 108].
![Working Capital and Asset Utilization](Screen%20Shots/5.png)

---

### 4. Interactive Financial Extractor Web App (`Financial_Extractor_Deploy`)
Built a **Streamlit** web application allowing users to enter one or multiple company ticker symbols, select the reporting period (Yearly/Quarterly), extract Income Statement, Balance Sheet, and Cash Flow data on demand, and download clean CSV files directly.

![Financial Extractor App](Screen%20Shots/app_interface.png)

---

## Tech Stack
- **Programming & Web App:** Python (`pandas`, `requests`, `SQLAlchemy`, `pyodbc`, `lxml`, `Streamlit`)[cite: 9, 109]
- **ETL & Database:** Microsoft SQL Server, SSIS
- **BI & Visualization:** Microsoft Power BI (Power Query, DAX, Star Schema Modeling)
