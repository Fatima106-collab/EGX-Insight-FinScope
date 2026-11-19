import os
import io
import time
import re
from html import unescape

import pandas as pd
import requests
import streamlit as st
from playwright.sync_api import sync_playwright

try:
    from curl_cffi import requests as curl_requests
except ImportError:
    curl_requests = None

# Portable output folder (works on any PC)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FOLDER = os.path.join(BASE_DIR, "output")

os.makedirs(SAVE_FOLDER, exist_ok=True)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Financial Extractor",
    page_icon="📊",
    layout="centered"
)


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

html,
body,
[data-testid="stAppViewContainer"],
.stApp {
    background-color: #f4f7fb !important;
    color: #17253a !important;
}

.main .block-container {
    max-width: 900px;
    padding-top: 35px;
    padding-bottom: 40px;
}


/* =========================
   LOGO
========================= */

.logo-box {
    width: 52px;
    height: 52px;
    background: #244a73;
    color: white !important;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 18px;
    margin: 0 auto 12px auto;
}


/* =========================
   HEADER
========================= */

.main-title {
    text-align: center;
    font-size: 38px;
    font-weight: 800;
    color: #17253a !important;
    margin-bottom: 6px;
}

.subtitle {
    text-align: center;
    color: #6c7888 !important;
    font-size: 15px;
    margin-bottom: 28px;
}


/* =========================
   LABELS
========================= */

label,
label p {
    color: #17253a !important;
    font-weight: 600 !important;
}


/* =========================
   TEXT INPUT
========================= */

div[data-testid="stTextInput"] input {
    color: #17253a !important;
    background-color: #eef4ff !important;
    border-radius: 10px !important;
    min-height: 42px !important;
    -webkit-text-fill-color: #17253a !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #8793a3 !important;
    opacity: 1 !important;
    -webkit-text-fill-color: #8793a3 !important;
}


/* =========================
   CAPTION
========================= */

div[data-testid="stCaptionContainer"],
div[data-testid="stCaptionContainer"] p {
    color: #6c7888 !important;
}


/* =========================
   FORM CARD
========================= */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #ffffff !important;
    border-radius: 18px !important;
    border: 1px solid #e1e7ee !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.05);
}


/* =========================
   EXTRACT BUTTON
========================= */

div.stButton > button {
    width: 100%;
    background-color: #244a73 !important;
    color: white !important;
    border-radius: 9px !important;
    border: none !important;
    height: 44px;
    font-weight: 700;
    font-size: 15px;
}

div.stButton > button:hover {
    background-color: #1d3d60 !important;
    color: white !important;
}

div.stButton > button p {
    color: white !important;
}


/* =========================
   SUCCESS
========================= */

.success-banner {
    background-color: #eaf7ee;
    color: #188143 !important;
    padding: 14px 16px;
    border-radius: 10px;
    margin-top: 16px;
    margin-bottom: 16px;
    font-size: 14px;
}


/* =========================
   COMPANY CARD
========================= */

.company-card {
    background-color: #eef9f2;
    border: 1px solid #d7eedf;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
}

.company-name {
    font-weight: 800;
    font-size: 15px;
    color: #1d2c3d !important;
}

.company-rows {
    color: #6f7b89 !important;
    font-size: 12px;
    margin-top: 2px;
}


/* =========================
   DOWNLOAD BUTTON
========================= */

div[data-testid="stDownloadButton"] button {
    background-color: #168544 !important;
    color: white !important;
    border: none !important;
    border-radius: 9px !important;
    height: 38px;
    font-weight: 700;
    width: 100%;
}

div[data-testid="stDownloadButton"] button:hover {
    background-color: #116b36 !important;
    color: white !important;
}

div[data-testid="stDownloadButton"] button p {
    color: white !important;
}


/* =========================
   FOOTER
========================= */

.footer {
    text-align: center;
    color: #9aa4b2 !important;
    font-size: 12px;
    margin-top: 30px;
}


/* ======================================================
   DROPDOWN FIX
   KEEP THIS AT THE END
====================================================== */

div[data-testid="stSelectbox"] {
    color-scheme: light !important;
}

div[data-testid="stSelectbox"]
div[data-baseweb="select"] > div {
    background: #ffffff !important;
    background-color: #ffffff !important;
    color: #17253a !important;
    -webkit-text-fill-color: #17253a !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
    min-height: 42px !important;
    color-scheme: light !important;
}

div[data-testid="stSelectbox"]
div[data-baseweb="select"] {
    background-color: #ffffff !important;
    color: #17253a !important;
    color-scheme: light !important;
}

div[data-testid="stSelectbox"]
div[data-baseweb="select"] * {
    color: #17253a !important;
    -webkit-text-fill-color: #17253a !important;
}

div[data-testid="stSelectbox"]
div[data-baseweb="select"] span {
    color: #17253a !important;
    -webkit-text-fill-color: #17253a !important;
}

div[data-testid="stSelectbox"] svg {
    color: #17253a !important;
    fill: #17253a !important;
}

div[data-baseweb="popover"] {
    background: #ffffff !important;
    background-color: #ffffff !important;
    color: #17253a !important;
    color-scheme: light !important;
}

div[data-baseweb="menu"] {
    background: #ffffff !important;
    background-color: #ffffff !important;
    color: #17253a !important;
    color-scheme: light !important;
}

ul[role="listbox"],
div[role="listbox"] {
    background: #ffffff !important;
    background-color: #ffffff !important;
    color: #17253a !important;
}

ul[role="listbox"] li,
div[role="option"] {
    background-color: #ffffff !important;
    color: #17253a !important;
}

ul[role="listbox"] li *,
div[role="option"] * {
    color: #17253a !important;
    -webkit-text-fill-color: #17253a !important;
}

ul[role="listbox"] li:hover,
div[role="option"]:hover {
    background-color: #eef4ff !important;
    color: #17253a !important;
}

ul[role="listbox"] li[aria-selected="true"],
div[role="option"][aria-selected="true"] {
    background-color: #e1ebfa !important;
    color: #17253a !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# REQUEST SETTINGS
# =========================================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),

    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,*/*;q=0.8"
    ),

    "Accept-Language": "en-US,en;q=0.9",
}


# =========================================================
# PERIODS
# =========================================================

PERIODS = {
    "Yearly": "",
    "Quarterly": "?p=quarterly",
    "TTM": "?p=trailing",
}


# =========================================================
# URLs
# =========================================================

def get_statement_urls(ticker, period_query):

    ticker = ticker.lower().strip()

    return {
        "Income Statement": (
            f"https://stockanalysis.com/quote/egx/"
            f"{ticker}/financials/income-statement/"
            f"{period_query}"
        ),

        "Balance Sheet": (
            f"https://stockanalysis.com/quote/egx/"
            f"{ticker}/financials/balance-sheet/"
            f"{period_query}"
        ),

        "Cash Flow": (
            f"https://stockanalysis.com/quote/egx/"
            f"{ticker}/financials/cash-flow-statement/"
            f"{period_query}"
        ),
    }


# =========================================================
# DOWNLOAD PAGE
# =========================================================
def download_page(url):
    """
    Download StockAnalysis page using real browser session
    to avoid 403 blocks.
    """

    try:
        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled"
                ]
            )

            page = browser.new_page(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "Chrome/120 Safari/537.36"
                )
            )

            page.goto(
                url,
                wait_until="networkidle",
                timeout=90000
            )

            page.wait_for_timeout(5000)

            html = page.content()

            browser.close()

            return html

    except Exception as e:
        raise Exception(
            f"Browser download failed: {e}"
        )


# =========================================================
# FLATTEN COLUMNS
# =========================================================

def flatten_columns(df):

    df = df.copy()

    if isinstance(df.columns, pd.MultiIndex):

        new_cols = []

        for col in df.columns:

            parts = [
                str(x).strip()
                for x in col
                if str(x).strip().lower()
                not in ["nan", "none", ""]
            ]

            new_cols.append(
                " ".join(parts)
            )

        df.columns = new_cols

    else:

        df.columns = [
            str(col).strip()
            for col in df.columns
        ]

    return df


# =========================================================
# CLEAN DATA
# =========================================================

def clean_dataframe(df):

    df = flatten_columns(df)

    df = df.dropna(how="all")

    df = df.drop_duplicates()

    df = df.reset_index(drop=True)

    return df


# =========================================================
# COMBINE FINANCIAL TABLES
# =========================================================

def combine_financial_tables(tables):

    valid_tables = []

    for df in tables:

        if df.empty:
            continue

        df = flatten_columns(df)

        rows, cols = df.shape

        if rows < 2 or cols < 4:
            continue

        df = df.dropna(how="all")

        df = df.reset_index(drop=True)

        valid_tables.append(df)


    if not valid_tables:

        raise ValueError(
            "No usable financial tables were found."
        )


    column_counts = {}

    for df in valid_tables:

        cols = df.shape[1]

        column_counts[cols] = (
            column_counts.get(cols, 0) + 1
        )


    most_common_col_count = max(
        column_counts,
        key=column_counts.get
    )


    compatible_tables = [
        df
        for df in valid_tables
        if df.shape[1] == most_common_col_count
    ]


    if not compatible_tables:

        raise ValueError(
            "No compatible financial tables found."
        )


    reference_columns = (
        compatible_tables[0].columns
    )


    normalized_tables = []

    for df in compatible_tables:

        df = df.copy()

        df.columns = reference_columns

        normalized_tables.append(df)


    combined_df = pd.concat(
        normalized_tables,
        ignore_index=True
    )


    combined_df = combined_df.drop_duplicates()

    combined_df = combined_df.dropna(how="all")

    combined_df = combined_df.reset_index(drop=True)


    return combined_df


# =========================================================
# SCRAPE ONE STATEMENT
# =========================================================

def scrape_statement(
    ticker,
    statement_name,
    url
):

    html = download_page(url)

    tables = pd.read_html(
        io.StringIO(html)
    )

    df = combine_financial_tables(
        tables
    )

    df = clean_dataframe(df)

    return df


# =========================================================
# GET COMPANY NAME
# =========================================================

def get_company_name(ticker):

    ticker = ticker.strip().upper()

    url = (
        f"https://stockanalysis.com/quote/egx/"
        f"{ticker.lower()}/"
    )

    try:

        html = download_page(url)

        # Read the HTML title.
        match = re.search(
            r"<title[^>]*>(.*?)</title>",
            html,
            flags=re.IGNORECASE | re.DOTALL
        )

        if not match:
            return ticker

        page_title = unescape(
            re.sub(
                r"\s+",
                " ",
                match.group(1)
            ).strip()
        )

        # Example:
        # Apple Inc. (AAPL) Stock Price & Overview

        ticker_pattern = re.escape(ticker)

        name_match = re.search(
            rf"^(.*?)\s*\({ticker_pattern}\)",
            page_title,
            flags=re.IGNORECASE
        )

        if name_match:

            company_name = (
                name_match.group(1).strip()
            )

            if company_name:
                return company_name

    except Exception:
        pass

    # Fallback if company name cannot be fetched.
    return ticker


# =========================================================
# SCRAPE COMPANY
# =========================================================

def scrape_company(
    ticker,
    period_query
):

    ticker = ticker.strip().upper()

    # Get company name once.
    company_name = get_company_name(
        ticker
    )

    urls = get_statement_urls(
        ticker,
        period_query
    )

    results = {}

    for statement_name, url in urls.items():

        df = scrape_statement(
            ticker=ticker,
            statement_name=statement_name,
            url=url
        )

        # =================================================
        # ADD COMPANY NAME COLUMN
        # =================================================

        # Prevent duplicate column if the function
        # is called again for any reason.
        if "Company Name" in df.columns:
            df = df.drop(
                columns=["Company Name"]
            )

        # Add Company Name as FIRST column.
        df.insert(
            0,
            "Company Name",
            company_name
        )

        results[statement_name] = df

        time.sleep(1)

    return results


# =========================================================
# CREATE CSV
# =========================================================

def create_csv_file(ticker, statements):

    rows = []

    for statement_name, df in statements.items():

        df = df.copy()

        if len(df.columns) < 2:
            continue

        line_item_col = df.columns[0]

        for _, row in df.iterrows():

            for period_col in df.columns[1:]:

                rows.append({
                    "Company": ticker,
                    "Statement": statement_name,
                    "Line_Item": row[line_item_col],
                    "Period": period_col,
                    "Amount": row[period_col]
                })

    final_df = pd.DataFrame(rows)

    final_df = final_df.drop_duplicates()
    final_df = final_df.dropna(how="all")

    return final_df


def save_csv_to_fixed_folder(ticker, period, csv_df):

    filename = (
        f"{ticker.upper()}_"
        f"{period.lower()}_"
        f"financials.csv"
    )

    filepath = os.path.join(SAVE_FOLDER, filename)

    csv_df.to_csv(
        filepath,
        index=False,
        encoding="utf-8-sig"
    )

    return filepath


# =========================================================
# SESSION STATE
# =========================================================

if "results" not in st.session_state:

    st.session_state.results = {}


if "period" not in st.session_state:

    st.session_state.period = None


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="logo-box">EGX</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="main-title">'
    'Financial Extractor'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="subtitle">'
    'Extract EGX Income Statement, Balance Sheet and Cash Flow '
    'data from StockAnalysis and download them as CSV.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# FORM
# =========================================================

with st.container(border=True):

    col1, col2 = st.columns(2)


    with col1:

        companies_input = st.text_input(
            "Company Code(s)",
            placeholder="COMI, SWDY, TMGH"
        )


        st.caption(
            "One EGX ticker, or several separated by commas. "
            "Example: COMI, SWDY, TMGH"
        )


    with col2:

        period = st.selectbox(
            "Financial Period",
            options=[
                "Yearly",
                "Quarterly",
                "TTM"
            ],
            index=0
        )


        st.caption(
            "Choose the required reporting period."
        )


    extract_button = st.button(
        "Extract Financials",
        use_container_width=True
    )


# =========================================================
# EXTRACTION
# =========================================================

if extract_button:

    tickers = [
        x.strip().upper()
        for x in companies_input.split(",")
        if x.strip()
    ]


    if not tickers:

        st.warning(
            "Please enter at least one company ticker."
        )


    else:

        period_query = PERIODS[period]

        st.session_state.results = {}

        st.session_state.period = period


        progress = st.progress(0)


        for i, ticker in enumerate(
            tickers,
            start=1
        ):

            try:

                with st.spinner(
                    f"Extracting {ticker}..."
                ):

                    statements = scrape_company(
                        ticker=ticker,
                        period_query=period_query
                    )


                    csv_df = create_csv_file(
                        ticker=ticker,
                        statements=statements
                    )

                    saved_path = save_csv_to_fixed_folder(
                        ticker=ticker,
                        period=period,
                        csv_df=csv_df
                    )


                    total_rows = sum(
                        len(df)
                        for df in statements.values()
                    )


                    st.session_state.results[
                        ticker
                    ] = {

                        "statements": statements,

                        "csv": csv_df.to_csv(index=False, encoding="utf-8-sig"),

                        "rows": total_rows,
                        "saved_path": saved_path,
                    }


            except Exception as e:

                st.error(
                    f"{ticker}: {e}"
                )


            progress.progress(
                int(
                    (i / len(tickers)) * 100
                )
            )


        progress.empty()


# =========================================================
# RESULTS
# =========================================================

if st.session_state.results:

    count = len(
        st.session_state.results
    )


    success_html = (
        f'<div class="success-banner">'
        f'Extraction completed successfully for '
        f'{count} compan{"y" if count == 1 else "ies"}.'
        f'</div>'
    )


    st.markdown(
        success_html,
        unsafe_allow_html=True
    )


    for ticker, data in (
        st.session_state.results.items()
    ):

        col_left, col_right = st.columns(
            [4, 1],
            vertical_alignment="center"
        )


        with col_left:

            company_html = (
                f'<div class="company-card">'
                f'<div class="company-name">{ticker}</div>'
                f'<div class="company-rows">'
                f'{data["rows"]} rows extracted'
                f'</div>'
                f'</div>'
            )


            st.markdown(
                company_html,
                unsafe_allow_html=True
            )

            st.caption(
                f'Automatically saved to: {data["saved_path"]}'
            )


        with col_right:

            st.download_button(
                label="Download",
                data=data["csv"],
                file_name=(
                    f"{ticker}_"
                    f"{st.session_state.period.lower()}_"
                    f"financials.csv"
                ),
                mime="text/csv",
                key=f"download_{ticker}",
                use_container_width=True
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">'
    'Financial Extractor'
    '</div>',
    unsafe_allow_html=True
)
