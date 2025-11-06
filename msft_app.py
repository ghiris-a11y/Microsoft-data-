#!/usr/bin/env python
# coding: utf-8

# In[2]:


# In[2]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# In[3]:
# Sidebar file upload
import streamlit as st
import pandas as pd

# Display Microsoft logo
st.image("https://logo.clearbit.com/microsoft.com", width=120)

# Sidebar file upload

st.sidebar.write("### Upload Your Financial Data")
uploaded_cashflow = st.sidebar.file_uploader("Upload Cash Flow CSV", type=["csv"])
uploaded_income = st.sidebar.file_uploader("Upload Income Statement CSV", type=["csv"])
uploaded_balance = st.sidebar.file_uploader("Upload Balance Sheet CSV", type=["csv"])


# Load data: use uploaded files if provided, else default
if uploaded_cashflow:
    cf = pd.read_csv(uploaded_cashflow)
else:
    cf = pd.read_csv("msft_cashflow.csv")

if uploaded_income:
    income = pd.read_csv(uploaded_income)
else:
    income = pd.read_csv("msft_income_statement.csv")

if uploaded_balance:
    bs = pd.read_csv(uploaded_balance)
else:
    bs = pd.read_csv("msft_balance_sheet.csv")

ratios = pd.read_csv("msft_ratios(1).csv", index_col=0)

# Tabs for navigation
tab1, tab2, tab3,tab4, tab5, tab6 = st.tabs(["Overview", "Ratios","DCF", "Multiples", "Dividend Model", "Scenario Analysis"])

income = pd.read_csv("msft_income_statement.csv", index_col=0)
bs = pd.read_csv("msft_balance_sheet.csv", index_col=0)
cf = pd.read_csv("msft_cashflow.csv", index_col=0)
ratios = pd.read_csv("msft_ratios(1).csv", index_col=0)

# ---------------- Overview Tab ----------------
with tab1:
    st.title("Microsoft Financial Overview")
    st.write("### Income Statement")
    st.dataframe(income.tail())
    st.write("### Balance Sheet")
    st.dataframe(bs.tail())
    st.write("### Cash Flow")
    st.dataframe(cf.tail())

    # KPI Cards
st.write("### Key Metrics")
st.metric("Revenue", f"${income['Total Revenue'].iloc[-1]:,.0f}")
st.metric("Net Income", f"${income['Net Income'].iloc[-1]:,.0f}")

# ---------------- Ratios Tab ----------------
with tab2:
    st.title("Financial Ratios")
    st.dataframe(ratios)

    st.write("### Ratio Trends")
    selected_ratio = st.selectbox("Select a ratio to plot", ratios.columns)
    st.line_chart(ratios[selected_ratio])

    # Download button
    st.download_button("Download Ratios CSV", ratios.to_csv().encode('utf-8'), "ratios.csv", "text/csv")

    # Interpretation
    st.write("### Interpretation")
    st.write("""
    **Profitability Ratios**:
    - **Gross Margin**: High margin (>60%) shows strong pricing power and cost control.
    - **Operating Margin**: Consistently high margins (>30%) suggest strong core business performance.
    - **Net Margin**: High net margins (>25%) indicate robust financial health.

    **Liquidity Ratios**:
    - **Current Ratio**: Around 2 means Microsoft can comfortably meet short-term obligations.

    **Leverage Ratios**:
    - **Debt-to-Equity**: Low ratio (<1) means Microsoft relies more on equity than debt.

    **Efficiency Ratios**:
    - **Asset Turnover**: Stable ratio indicates efficient asset utilization.
    """)


# ---------------- DCF ----------------
with tab3:
    st.subheader("Discounted Cash Flow (DCF)")
    cf = cf.dropna(subset=["Free Cash Flow"])
    last_fcf = cf["Free Cash Flow"].iloc[-1] / 1_000_000_000  # Convert to billions

    discount_rate = st.slider("Discount Rate", 0.05, 0.15, 0.10)
    growth_rate = st.slider("Growth Rate", 0.01, 0.08, 0.03)
    years = st.slider("Projection Years", 3, 10, 5)

    projected_fcfs = [last_fcf * ((1 + growth_rate) ** i) for i in range(1, years + 1)]
    discounted_fcfs = [fcf / ((1 + discount_rate) ** i) for i, fcf in enumerate(projected_fcfs, 1)]
    terminal_value = projected_fcfs[-1] * (1 + growth_rate) / (discount_rate - growth_rate)
    discounted_terminal = terminal_value / ((1 + discount_rate) ** years)
    dcf_value = sum(discounted_fcfs) + discounted_terminal

    st.metric("Estimated DCF Value", f"${dcf_value:,.2f} Billion")

    # Interpretation
    st.write("### Interpretation")
    st.write(f"""
    Under the assumptions of a {discount_rate*100:.0f}% discount rate and {growth_rate*100:.0f}% growth rate,
    Microsoft's intrinsic value is estimated at **${dcf_value:,.2f} Billion**.

    - **Current Market Cap**: ~3,000 Billion (approx $3 trillion)
    - **Comparison**: The DCF estimate is slightly below the current market cap, suggesting the stock may be fairly valued or slightly overvalued.
    - **Sensitivity**: Increasing discount rate or lowering growth would reduce this valuation significantly.
    """)

# ---------------- Multiples ----------------
with tab4:
    st.subheader("Comparable Multiples")
    ticker = "MSFT"
    stock = yf.Ticker(ticker)
    price = stock.history(period="1d")["Close"].iloc[-1]
    pe_ratio = stock.info.get("trailingPE", "N/A")
    pb_ratio = stock.info.get("priceToBook", "N/A")
    ps_ratio = stock.info.get("priceToSalesTrailing12Months", "N/A")

    st.write(f"**Current Price:** ${price:,.2f}")
    st.write(f"**P/E Ratio:** {pe_ratio}")
    st.write(f"**P/B Ratio:** {pb_ratio}")
    st.write(f"**P/S Ratio:** {ps_ratio}")

    # Interpretation
    st.write("### Interpretation")
    st.write("""
    - **P/E Ratio**: Indicates how much investors are willing to pay per dollar of earnings. A high P/E suggests growth expectations.
    - **P/B Ratio**: Shows valuation relative to book value. Lower ratios may indicate undervaluation.
    - **P/S Ratio**: Useful for companies with volatile earnings; compares price to revenue.
    """)

# ---------------- Dividend Discount Model ----------------
with tab5:
    st.subheader("Dividend Discount Model (DDM)")
    dividend = stock.info.get("dividendRate", 0)
    if dividend > 0:
        ddm_value = dividend * (1 + growth_rate) / (discount_rate - growth_rate)
        st.metric("Estimated DDM Value", f"${ddm_value:,.2f}")
        st.write("""
        Interpretation:
        - DDM is suitable for dividend-paying companies.
        - Higher growth or lower discount rate increases valuation.
        """)
    else:
        st.warning("Microsoft does not pay significant dividends for DDM valuation.")

# ---------------- Scenario Analysis ----------------
with tab6:
    st.subheader("Scenario Analysis")
    scenarios = {
        "Best Case": {"growth": 0.05, "discount": 0.08},
        "Base Case": {"growth": 0.03, "discount": 0.10},
        "Worst Case": {"growth": 0.01, "discount": 0.12}
    }
    results = {}
    for case, params in scenarios.items():
        projected_fcfs = [last_fcf * ((1 + params["growth"]) ** i) for i in range(1, years + 1)]
        discounted_fcfs = [fcf / ((1 + params["discount"]) ** i) for i, fcf in enumerate(projected_fcfs, 1)]
        terminal_value = projected_fcfs[-1] * (1 + params["growth"]) / (params["discount"] - params["growth"])
        discounted_terminal = terminal_value / ((1 + params["discount"]) ** years)
        results[case] = sum(discounted_fcfs) + discounted_terminal

    st.write(pd.DataFrame.from_dict(results, orient="index", columns=["Valuation (Billion $)"]))
    st.bar_chart(pd.DataFrame.from_dict(results, orient="index"))

    st.write("""
    Interpretation:
    - **Best Case** assumes higher growth and lower discount rate → highest valuation.
    - **Worst Case** assumes lower growth and higher discount rate → lowest valuation.
    - Scenario analysis helps visualize sensitivity to assumptions.
    """)








