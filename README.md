<img width="1158" height="807" alt="3" src="https://github.com/user-attachments/assets/6f1f4785-5faa-4c3e-a23e-8b907ca7cf39" /># EGX Insight – FinScope (End-to-End Financial & Stock Market Analysis)

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
Tracks core KPIs (Revenue, EBITDA, Net Income, Operating & Free Cash Flow, ROE), margin evolution, cash vs. net debt, and cash generation trends.
( <img width="1156" height="804" alt="1" src="https://github.com/user-attachments/assets/d23f7741-a263-4bdf-a2fe-787cb7dc92af" />
)

#### Page 2: P&L & Cost Structure Analysis
Provides a detailed Profit & Loss statement matrix, YoY/QoQ revenue and cost growth cards, a P&L Waterfall bridge from Revenue to Net Income, and profitability breakdown

(<img width="1164" height="796" alt="2" src="https://github.com/user-attachments/assets/94e0331d-e482-4052-827e-f392e7abd484" />
)

#### Page 3: Financial Position & Capital Structure
Visualizes Assets, Liabilities, and Shareholders' Equity composition and historical mix alongside leverage metrics (Debt-to-Equity, Debt-to-Assets, Net Debt/EBITDA)

( <img width="1158" height="807" alt="3" src="https://github.com/user-attachments/assets/c1efeaaa-48bd-4a3e-b132-7760d6fc942d" />)


#### Page 4: Liquidity, Solvency & Financial Leverage
Monitors Current, Quick, and Cash ratios, Working Capital, Interest Coverage, Debt Capacity (EBITDA vs. Interest Expense), and debt maturity trends[cite: 107].

(<img width="1156" height="806" alt="4" src="https://github.com/user-attachments/assets/83b21c6b-f7b1-4f41-beb9-c51cd966a571" />
)

#### Page 5: Working Capital & Asset Utilization
Analyzes Net Working Capital components (AR, Inventory, AP), Cash Conversion Cycle (DSO, DIO, DPO), and asset turnover efficiency
 
(<img width="1153" height="795" alt="5" src="https://github.com/user-attachments/assets/ceb90b43-6650-4dda-8620-3b0fa8f266ff" />
)

---

### 4. Interactive Financial Extractor Web App (`Financial_Extractor_Deploy`)
Built a **Streamlit** web application allowing users to enter one or multiple company ticker symbols, select the reporting period (Yearly/Quarterly), extract Income Statement, Balance Sheet, and Cash Flow data on demand, and download clean CSV files directly.

(<img width="1920" height="989" alt="Screenshot 2026-09-09 194843" src="https://github.com/user-attachments/assets/5739a2dc-423c-4a2c-b6a2-572ddd10f4d2" />
)

---

## Tech Stack
- **Programming & Web App:** Python (`pandas`, `requests`, `SQLAlchemy`, `pyodbc`, `lxml`, `Streamlit`)[cite: 9, 109]
- **ETL & Database:** Microsoft SQL Server, SSIS
- **BI & Visualization:** Microsoft Power BI (Power Query, DAX, Star Schema Modeling)
