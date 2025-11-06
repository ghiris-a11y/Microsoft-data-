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


# In[9]:


if section == "Valuation":
    st.title("DCF Valuation")

    last_fcf = cf["Free Cash Flow"].iloc[-1
    discount_rate = 0.08
    growth_rate = 0.05
    years = 5

    projected_fcfs = [last_fcf * ((1 + growth_rate) ** i) for i in range(1, years + 1)]
    discounted_fcfs = [fcf / ((1 + discount_rate) ** i) for i, fcf in enumerate(projected_fcfs, 1)]

    terminal_value = projected_fcfs[-1] * (1 + growth_rate) / (discount_rate - growth_rate)
    discounted_terminal = terminal_value / ((1 + discount_rate) ** years)

    dcf_value = sum(discounted_fcfs) + discounted_terminal

    st.metric(label="Estimated DCF Value", value=f"${dcf_value:,.2f}")


# In[ ]:




