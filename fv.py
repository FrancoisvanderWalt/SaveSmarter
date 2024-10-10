import streamlit as st
import datetime
import numpy as np

st.markdown(
    """
    <style>
    body {
        background-color: #000000;
        color: #ffffff;
    }
    .stApp {
        background-color: #000000;
    }
    .stSidebar {
        background-color: #000000;
    }
    .stButton > button {
        background-color: #ff00ff;
        color: #ffffff;
        border-radius: 5px;
        border: none;
    }
    input {
        background-color: #00ffff;
        color: #000000;
    }
    .stDateInput input {
        background-color: #00ffff;
        color: #000000;
    }
    .stNumberInput input {
        background-color: #00ffff;
        color: #000000;
    }
    .stSelectbox div[data-baseweb='select'] {
        background-color: #00ffff !important;
        color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.image('∑.png', width=200)
st.markdown("<h4 style='font-size: 16px; color: #ff00ff; margin-top: -10px; margin-bottom: 20px;'>Save like a Sigma</h4>", unsafe_allow_html=True)

current_balance = st.number_input("Current Savings Balance (in R)", min_value=0.0, step=100.0, value=0.0, format="%.2f", key="current_balance")
interest_rate = st.number_input("Annual Interest Rate (in %)", min_value=0.0, step=1.0, value=0.0, format="%.2f", key="interest_rate")
target_value = st.number_input("Target Savings Value (in R)", min_value=0.0, step=100.0, value=0.0, format="%.2f", key="target_value")
start_date = st.date_input("First Date for Deposit", min_value=datetime.date.today() + datetime.timedelta(days=1), max_value=target_date - datetime.timedelta(days=1))
target_date = st.date_input("Target Date", min_value=datetime.date.today() + datetime.timedelta(days=2))
deposit_period = st.selectbox("Period of Deposits", ["Daily", "Weekly", "Monthly"])

current_date = datetime.date.today()
days_remaining = (target_date - start_date).days
months_remaining = (target_date.year - current_date.year) * 12 + (target_date.month - current_date.month)
years_remaining = days_remaining / 365.0

if deposit_period == "Daily":
    deposit_periods_per_year = 365
    deposit_frequency = 1
elif deposit_period == "Weekly":
    deposit_periods_per_year = 52
    deposit_frequency = 7
else:
    deposit_periods_per_year = 12
    deposit_frequency = 30

total_deposit_periods = max(1, days_remaining // deposit_frequency)

compounding_periods_per_year = 12
rate_per_period = (interest_rate / 100) / compounding_periods_per_year

future_value = current_balance * ((1 + rate_per_period) ** months_remaining)

if target_value > 0 and future_value >= target_value and current_balance > 0 and interest_rate > 0 and start_date < target_date:
    st.write(f"Based on your current balance and interest rate, you will reach your target without any additional deposits. By {target_date}, your estimated balance will be R{future_value:,.2f}.")
else:
    if interest_rate > 0:
        fv_needed = target_value - future_value
        r = (interest_rate / 100) / deposit_periods_per_year
        n = total_deposit_periods

        if r > 0 and n > 0:
            required_deposit = fv_needed * r / (((1 + r) ** n) - 1)
        else:
            required_deposit = fv_needed / n if n > 0 else 0.0
    else:
        required_deposit = (target_value - future_value) / total_deposit_periods if total_deposit_periods > 0 else 0.0
    
    if required_deposit > 0 and current_balance > 0 and interest_rate >= 0 and target_value > 0 and start_date < target_date:
        period_label = 'day' if deposit_period == 'Daily' else ('week' if deposit_period == 'Weekly' else 'month')
        st.write(f"To reach your target of R{target_value:,.2f} by {target_date}, you will need to deposit R{required_deposit:,.2f} every {period_label}. This will require {total_deposit_periods} deposits over a period of {days_remaining} days.")
    else:
        st.write("Your current balance and interest rate are sufficient to reach your target without additional deposits.")