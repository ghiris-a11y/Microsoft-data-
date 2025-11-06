#!/usr/bin/env python
# coding: utf-8

# In[2]:


# In[2]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# In[3]:



income = pd.read_csv("msft_income_statement.csv", index_col=0)
bs = pd.read_csv("msft_balance_sheet.csv", index_col=0)
cf = pd.read_csv("msft_cashflow.csv", index_col=0)
ratios = pd.read_csv("msft_ratios(1).csv", index_col=0)


# In[6]:





# In[7]:






# In[4]:



st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Overview", "Ratios", "Valuation"])


# In[5]:



if section == "Overview":
    st.title("Microsoft Financial Overview")
    st.write("### Income Statement")
    st.dataframe(income.tail())
    st.write("### Balance Sheet")
    st.dataframe(bs.tail())
    st.write("### Cash Flow")
    st.dataframe(cf.tail())


# In[7]:



if section == "Ratios":
    st.title("Financial Ratios")
    st.dataframe(ratios)

    st.write("### Ratio Trends")
    selected_ratio = st.selectbox("Select a ratio to plot", ratios.columns)
    st.line_chart(ratios[selected_ratio])

    # ✅ Add interpretation text
    st.write("### Interpretation")
    st.write("""
    **Profitability Ratios**:
    - **Gross Margin**: Indicates how efficiently Microsoft converts revenue into gross profit. A high margin (>60%) shows strong pricing power and cost control.
    - **Operating Margin**: Reflects operational efficiency. Consistently high margins (>30%) suggest strong core business performance.
    - **Net Margin**: Shows overall profitability after all expenses. High net margins (>25%) indicate robust financial health.

    **Liquidity Ratios**:
    - **Current Ratio**: Measures short-term solvency. A ratio around 2 means Microsoft can comfortably meet short-term obligations.

    **Leverage Ratios**:
    - **Debt-to-Equity**: Indicates financial risk. A low ratio (<1) means Microsoft relies more on equity than debt, reducing risk.

    **Efficiency Ratios**:
    - **Asset Turnover**: Shows how effectively assets generate revenue. A stable ratio indicates efficient asset utilization.

    Overall, Microsoft’s ratios suggest strong profitability, healthy liquidity, and conservative leverage, supporting its position as a financially robust company.
    """)


# In[9]:


if section == "Valuation":
    st.title("DCF Valuation")

    try:
        cf = cf.dropna(subset=["Free Cash Flow"])
        last_fcf = cf["Free Cash Flow"].iloc[-1] / 1_000_000_000  # Convert to billions

        discount_rate = 0.10  # 10%
        growth_rate = 0.03    # 3%
        years = 5

        projected_fcfs = [last_fcf * ((1 + growth_rate) ** i) for i in range(1, years + 1)]
        discounted_fcfs = [fcf / ((1 + discount_rate) ** i) for i, fcf in enumerate(projected_fcfs, 1)]

        terminal_value = projected_fcfs[-1] * (1 + growth_rate) / (discount_rate - growth_rate)
        discounted_terminal = terminal_value / ((1 + discount_rate) ** years)

        dcf_value = sum(discounted_fcfs) + discounted_terminal
        st.metric(label="Estimated DCF Value", value=f"${dcf_value:,.2f} Billion")

        # ✅ Add interpretation text
        st.write("### Interpretation")
        st.write(f"""
        Under the assumptions of a {discount_rate*100:.0f}% discount rate and {growth_rate*100:.0f}% growth rate,
        Microsoft's intrinsic value is estimated at **${dcf_value:,.2f} Billion**.
        
        - **Current Market Cap**: ~3,000 Billion (approx \$3 trillion)
        - **Comparison**: The DCF estimate is slightly below the current market cap, suggesting the stock may be fairly valued or slightly overvalued.
        - **Sensitivity**: Increasing discount rate or lowering growth would reduce this valuation significantly.
        """)
    except Exception as e:
        st.error(f"Error in DCF calculation: {e}")

# In[ ]:




