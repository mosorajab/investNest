# Investment and Inflation Calculator Web App
import streamlit as st
import numpy as np
import datetime

import streamlit as st

def investment_calculator():
    st.header("🚀 Investment Calculator")
    # Input fields for investment parameters
    current_age = st.number_input("Current Age", min_value=0, value=00)
    retirement_age = st.number_input("Retirement Age", min_value=current_age + 1, value=00)
    initial_investment_amount = st.number_input("Initial Investment Amount", min_value=0.0, value=00, step=1000.0, format="%.2f")
    initial_monthly_investment = st.number_input("Initial Monthly Investment", min_value=0.0, value=00, step=100.0, format="%.2f")
    annual_increase_rate = st.number_input("Annual Increase Rate of Monthly Investment (%)", min_value=0.0, value=00.00, step=0.1, format="%.2f")
    annual_return_rate = st.number_input("Annual Return Rate (%)", min_value=0.0, value=0.0, step=0.1, format="%.2f")
    
    if st.button("Calculate Investment"):
        years_to_invest = retirement_age - current_age
        total_months = years_to_invest * 12
        monthly_return_rate = annual_return_rate / 12 / 100
        annual_increase_rate_decimal = annual_increase_rate / 100
        monthly_investment = initial_monthly_investment
        total_value = initial_investment_amount
        investment_values = []  # For plotting
        months = []
        
        for month in range(1, total_months + 1):
            total_value += monthly_investment
            total_value *= (1 + monthly_return_rate)
            if month % 12 == 0:
                monthly_investment *= (1 + annual_increase_rate_decimal)
            investment_values.append(total_value)
            months.append(month)
        
        st.success(f"🎉 At age {retirement_age}, you will have: ZAR {total_value:,.2f} 🎉")
        
        if total_value > 1000000:
            st.balloons()
        
        # Plot the investment growth over time
        st.line_chart(data=investment_values, width=0, height=0, use_container_width=True)
        st.caption("📊 Investment Growth Over Time (Months)")

def inflation_calculator():
    st.header("🎈 Inflation Calculator")
    # Input fields for inflation parameters
    amount = st.number_input("Enter the Amount of Money", min_value=0.0, value=55000000.0, step=1000.0, format="%.2f")
    target_year = st.number_input("Enter the Target Year", min_value=2024, value=2055, step=1)
    inflation_rate = st.number_input("Annual Inflation Rate (%)", min_value=0.0, value=3.0, step=0.1, format="%.2f")
    
    if st.button("Calculate Inflation Adjustment"):
        current_year = datetime.datetime.now().year
        years_difference = target_year - current_year
        inflation_rate_decimal = inflation_rate / 100
        # Adjust the amount for inflation
        adjusted_value = amount / ((1 + inflation_rate_decimal) ** years_difference)
        st.success(f"🎉 The amount of ZAR {amount:,.2f} in {target_year} will be worth ZAR {adjusted_value:,.2f} in {current_year} adjusted for inflation. 💰")

def main():
    st.title("Investment + Inflation Calculator")
    # Sidebar navigation
    # st.sidebar.title("")
    st.sidebar.image("assets/image.webp", caption="Choose your calculator", use_column_width=True)
    app_mode = st.sidebar.radio("Select Calculator", ["💰 Investment Calculator", "📈 Inflation Calculator"])
    
    if app_mode == "💰 Investment Calculator":
        investment_calculator()
    elif app_mode == "📈 Inflation Calculator":
        inflation_calculator()

if __name__ == "__main__":
    main()

    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: rgba(0, 0, 0, 0.1); /* More transparent */
            color: white;
            text-align: center;
            padding: 2px; /* Smaller padding */
            font-size: 10px; /* Smaller font size */
        }
        </style>
        <div class="footer">
            <p>built by msr</p>
        </div>
        """,
        unsafe_allow_html=True
    )
