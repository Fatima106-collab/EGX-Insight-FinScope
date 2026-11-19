import pandas as pd
import requests
import time
import io
import urllib
from sqlalchemy import create_engine
import sys

# ==========================================
# STEP 1: SET UP COMPANIES AND PERIOD
# ==========================================
banks_list = [
    "COMI", "QNBE", "HDBK", "ADIB", "CANA", "CIEB",
    "FAIT", "FAITA", "EXPA", "SAUD", "UBEE", "EGBE", "SAIB"
]
companies_list = [
    "SWDY", "TMGH", "ETEL", "EGAL", "MFPC", "EAST", "ABUK", "ALCN",
    "EFIH", "ORAS", "FWRY", "EMFD", "SCTS", "ORHD", "EFID", "PHDC",
    "VLMR", "VLMRA", "OCDI", "GPPL", "JUFO", "HRHO", "BIOC", "BTFH",
    "GBCO", "IRON", "FERC", "HELI", "RAYA", "EGCH", "ARCC", "SCEM",
    "CLHO", "VALU", "CCAP", "PHAR", "CIRA", "MCQE", "EFIC", "TAQA",
    "SKPC", "MBSC", "MTIE", "AMES", "POUL", "EGTS", "NIPH", "ORWE",
    "EGSA", "MASR", "MOIL", "AMOC", "MHOT", "TALM", "ATQA", "ISPH",
    "CICH", "RMDA", "CSAG", "BINV", "IFAP", "OIH", "MPRC", "PRDC",
    "OLFI", "MIPH", "MOIN", "BONY", "ISMQ", "PHTV", "MPCI", "EGAS",
    "AMIA", "SPHT", "DOMT", "CPCI", "ZMID", "KORA", "AFMC", "SUGR",
    "ELEC", "SPIN", "AXPH", "ACAP", "ENGC", "NAPR", "NINH", "GOUR",
    "OCPH", "CNFN", "ARAB", "AMER", "MICH", "DSCW", "KABO", "SVCE",
    "GSSC", "WCDF", "MFSC", "UNIT", "GDWA", "OFH", "KZPC", "ACGC",
    "AJWA", "UEFM", "SDTI", "CRST", "ADCI", "ELKA", "ISMA", "ACTF",
    "ASCM", "ELSH", "INFI", "GTWL", "NAHO", "ZEOT", "LCSW", "CFGH",
    "ALRA", "DAPH", "ACAMD", "SMFR", "ETRS", "EDFM", "MILS", "LUTS",
    "MPCO", "NARE", "CEFM", "EALR", "ATLC", "GPIM", "AALR", "PHGC",
    "CAED", "GGCC", "ADPC", "ODIN", "RACC", "EHDR", "ECAP", "MOSC",
    "GGRN", "IDRE", "WKOL", "SNFC", "MAAL", "MENA", "SCFM", "PRCL",
    "ICID", "DTPP", "UEGC", "NCCW", "DEIN", "NHPS", "CERA", "SEIG",
    "SEIGA", "OBRI", "MEPA", "SIPC", "NDRL", "ALUM", "AMII", "RREI",
    "AFDI", "COSG", "AIDC", "ASPI", "GTEX", "RTVC", "POCO", "EBSC",
    "KRDI", "TANM", "MCRO", "PRMH", "UNIP", "ROTO", "APSW", "KWIN",
    "MEGM", "RUBX", "TYCN", "ICLE", "SPMD", "MOED", "AIHC", "EASB",
    "EEII", "RAKT", "AREH", "CCRS", "EPCO", "GRCA", "GIHD", "ELWA",
    "ELNA", "DGTZ", "TRTO", "DCCC", "NEDA", "MMAT", "EPPK", "GMCI",
    "EOSB", "CPME", "COPR"
]

period_input = input("Enter period (yearly, quarterly, trailing): ")

statements = ["income-statement", "balance-sheet", "cash-flow-statement"]

if period_input == "quarterly":
    period_url = "?p=quarterly"
elif period_input == "trailing":
    period_url = "?p=trailing"
else:
    period_url = ""

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9"
}

# ==========================================
# STEP 2: CONNECT TO DATABASE ONCE AT THE START
# ==========================================
server = 'AR-L-6006'       
database = 'EGX_Data'  

print(f"\nConnecting to SQL Server database '{database}'...")
try:
    params = urllib.parse.quote_plus(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes;"
    )
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    
    # Test connection
    with engine.connect() as connection:
        pass
    print("Database connection successful!\n")
    
except Exception as e:
    print(f"Failed to connect to SQL Server. Error: {e}")
    sys.exit() # Stop the script completely if DB connection fails

# ==========================================
# STEP 3: SCRAPE, CLEAN, AND SAVE CONTINUOUSLY
# ==========================================
print(f"Starting download and database insertion for {len(companies_list)} companies...\n")

i = 1
total_requests = len(companies_list) * len(statements)

for company in companies_list:
    for statement in statements:
        url = f"https://stockanalysis.com/quote/egx/{company}/financials/{statement}/{period_url}"
        print(f"[{i}/{total_requests}] Fetching: {company} - {statement}...", end=" ")
        
        try:
            # 1. Download the webpage
            response = requests.get(url, headers=headers)
            all_tables = pd.read_html(io.StringIO(response.text))
            
            tables_to_combine = []
            if statement == "income-statement":
                tables_to_combine = [all_tables[0]]
            elif statement == "balance-sheet":
                tables_to_combine = all_tables[0:3]
            elif statement == "cash-flow-statement":
                tables_to_combine = all_tables[0:3]
            
            # 2. Standardize headers
            cleaned_tables = []
            for table in tables_to_combine:
                if isinstance(table.columns, pd.MultiIndex):
                    table.columns = table.columns.get_level_values(0)
                
                cols = list(table.columns)
                cols[0] = 'Line_Item'
                table.columns = cols
                cleaned_tables.append(table)
            
            # 3. Combine tables and remove duplicate columns
            df = pd.concat(cleaned_tables, ignore_index=True)
            df = df.loc[:, ~df.columns.duplicated()]
            df = df.dropna(how="all").drop_duplicates()
            
            # Insert columns while preserving the original layout order from the website
            df.insert(0, "Line_Order", range(1, len(df) + 1))
            df.insert(1, "Company", company.upper())
            df.insert(2, "Statement", statement)
            
            # 4. UNPIVOT THE DATA (Melt) for this single request
            melted_df = df.melt(
                id_vars=['Line_Order', 'Company', 'Statement', 'Line_Item'], 
                var_name='Period',
                value_name='Amount'
            )
            
            melted_df['Period'] = melted_df['Period'].astype(str)
            melted_df['Amount'] = melted_df['Amount'].astype(str).str.replace(',', '').str.replace('-', '0')
            melted_df['Amount'] = pd.to_numeric(melted_df['Amount'], errors='coerce')
            melted_df = melted_df.dropna(subset=['Amount'])
            
            # ---> NEW ADDITION: Sort the data by Rank (Line_Order) before inserting <---
            melted_df = melted_df.sort_values(by=['Line_Order', 'Period'], ascending=[True, False])
            
            # 5. Insert directly to Database
            if not melted_df.empty:
                melted_df.to_sql(
                    name='Staging_Financials', 
                    con=engine, 
                    if_exists='append', 
                    index=False
                )
                print("✅ Saved to DB.")
            else:
                print("⚠️ No valid data to save.")
            
        except Exception as e:
            print(f"⚠️ Error. Skipping...")
            
        i += 1
        time.sleep(1)

print("\nAll processes completed!")