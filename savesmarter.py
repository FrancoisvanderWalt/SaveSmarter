import streamlit as st
import datetime
from datetime import timedelta
import numpy as np

# Styling and UI customization
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
    .stNumberInput input {
        background-color: #00e0ff;
        color: #000000;
    }
    
    .stDateInput input {
        background-color: #00e0ff;
        color: #000000;
    }
    
    .stSelectbox div[data-baseweb='select'] {
        background-color: #00e0ff !important;
        color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header and description
st.markdown("<h1 style='font-size: 56px; color: #00e0ff; font-weight: 900; letter-spacing: 2px; text-shadow: 0 0 5px #00e0ff;'>Save Smarter</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='font-size: 16px; color: #ffffff; margin-top: -10px; margin-bottom: 20px;'>When you don't know how to reach your goals - we do.</h4>", unsafe_allow_html=True)

# Input fields
current_balance = st.number_input(
    "Current Savings Balance (in R)",
    min_value=0.0,
    step=100.0,
    format="%.2f",
    value=None, 
    placeholder="0.0",
    key="current_balance",
    help="The current balance you have saved towards your goal."
)

interest_rate = st.number_input(
    "Annual Interest Rate (in %)",
    min_value=0.0,
    step=1.0,
    format="%.2f",
    value=None,
    placeholder="0.0",
    key="interest_rate",
    help="The annual nominal interest rate, compounded monthly."
)

target_value = st.number_input(
    "Target Savings Value (in R)",
    min_value=0.0,
    step=100.0,
    format="%.2f",
    value=None,
    placeholder="0.0",
    key="target_value",
    help="The final savings amount you aim to reach by your target date."
)

# Date inputs
target_date = st.date_input(
    "Target Date",
    min_value=datetime.date.today() + datetime.timedelta(days=2),
    key='target_date',
    help="The deadline by which you intend to reach your savings target.",
    disabled=(current_balance is None or interest_rate is None or target_value is None)
)

start_date = st.date_input(
    "First Date for Deposit",
    min_value=datetime.date.today() + datetime.timedelta(days=1),
    max_value=target_date - datetime.timedelta(days=1),
    key='start_date',
    help="The starting date for making regular deposits towards your goal.",
    disabled=(current_balance is None or interest_rate is None or target_value is None)
)

# Period of deposits
deposit_period = st.selectbox(
    "Period of Deposits",
    ["Daily", "Weekly", "Monthly"],
    help="How often you plan to contribute to your savings (daily, weekly, or monthly).",
    disabled=(current_balance is None or interest_rate is None or target_value is None)
)

# Missing fields warning
missing_fields = []
if current_balance is None:
    missing_fields.append('Current Savings Balance')
if interest_rate is None:
    missing_fields.append('Annual Interest Rate')
if target_value is None:
    missing_fields.append('Target Savings Value')

if missing_fields:
    st.warning(f"Please enter valid values for: {', '.join(missing_fields)} to proceed.")
    st.stop()

# Calculations
current_date = datetime.date.today()
days_remaining = max(1, (target_date - start_date).days)
months_remaining = max(0, (target_date.year - current_date.year) * 12 + (target_date.month - current_date.month))
years_remaining = days_remaining / 365.0

# Determine deposit frequency
deposit_periods_per_year = {
    "Daily": 365,
    "Weekly": 52,
    "Monthly": 12
}[deposit_period]

deposit_frequency = {
    "Daily": 1,
    "Weekly": 7,
    "Monthly": 30
}[deposit_period]

date = start_date
total_deposit_periods = 0
while date < target_date:
    total_deposit_periods += 1
    date += timedelta(days=deposit_frequency)

# Compounding calculations
compounding_periods_per_year = 12
rate_per_period = (interest_rate / 100) / compounding_periods_per_year

future_value = (current_balance or 0) * ((1 + rate_per_period) ** months_remaining)

# Check if target can be met without additional deposits
if target_value > 0 and future_value >= target_value and interest_rate > 0 and start_date < target_date:
    st.success(f"Based on your current balance and interest rate, you will reach your target without any additional deposits. By {target_date}, your estimated balance will be R{future_value:,.2f}.")
else:
    # Calculate the required deposit per period using the future value of an annuity formula
    fv_needed = target_value - future_value
    r = (interest_rate / 100) / deposit_periods_per_year # Estimate interest for simplicity of demo
    n = total_deposit_periods

    if r > 0 and n > 0:
        required_deposit = fv_needed * r / (((1 + r) ** n) - 1) # FV annuity function
    else:
        required_deposit = fv_needed / n if n > 0 else 0.0

    if required_deposit > 0 and target_value > future_value:
        period_label = 'day' if deposit_period == 'Daily' else ('week' if deposit_period == 'Weekly' else 'month')
        st.info(f"To reach your target of R{target_value:,.2f} by {target_date}, you will need to deposit R{required_deposit:,.2f} every {period_label}. This will require {total_deposit_periods} deposits over a period of {days_remaining} days.")
    else:
        if target_value > 0 and future_value < target_value and current_balance > 0:
            st.warning("Your current balance and interest rate are insufficient to reach your target without additional deposits.")