# Investment and Inflation Calculator Web App
import streamlit as st
import numpy as np
import datetime

def investment_calculator():
    st.header("🚀 Investment Calculator")

    # Selection option
    calculation_type = st.radio("What would you like to calculate?", 
                                ["Future Value at Retirement", "Required Monthly Savings to Reach Goal"])

    # Common inputs
    current_age = st.number_input("Current Age", min_value=0, value=25)
    retirement_age = st.number_input("Retirement Age", min_value=current_age + 1, value=65)
    initial_investment_amount = st.number_input("Initial Investment Amount (ZAR)", min_value=0.0, value=50000.0, step=1000.0, format="%.2f")
    annual_return_rate = st.number_input("Annual Return Rate (%)", min_value=0.0, value=9.0, step=0.1, format="%.2f") / 100
    years_to_invest = retirement_age - current_age

    if calculation_type == "Future Value at Retirement":
        # Inputs specific to Future Value calculation
        initial_monthly_investment = st.number_input("Initial Monthly Investment (ZAR)", min_value=0.0, value=5000.0, step=100.0, format="%.2f")
        annual_increase_rate = st.number_input("Annual Increase Rate of Monthly Investment (%)", min_value=0.0, value=10.0, step=0.1, format="%.2f") / 100

        if st.button("Calculate Future Value"):
            total_value, investment_values = calculate_future_value(
                initial_investment_amount,
                initial_monthly_investment,
                annual_increase_rate,
                annual_return_rate,
                years_to_invest
            )
            st.success(f"🎉 At age {retirement_age}, you will have: ZAR {total_value:,.2f} 🎉")

            if total_value > 1000000:
                st.balloons()

            # Plot the investment growth over time
            st.line_chart(data=investment_values, use_container_width=True)
            st.caption("📊 Investment Growth Over Time (Months)")

    else:
        # Inputs specific to Required Monthly Savings calculation
        savings_goal = st.number_input("Savings Goal at Retirement (ZAR)", min_value=0.0, value=6000000.0, step=1000.0, format="%.2f")
        annual_increase_rate = st.number_input("Annual Increase Rate of Monthly Savings (%)", min_value=0.0, value=0.0, step=0.1, format="%.2f") / 100

        if st.button("Calculate Required Monthly Savings"):
            required_monthly_savings = calculate_required_monthly_savings(
                initial_investment_amount,
                savings_goal,
                annual_increase_rate,
                annual_return_rate,
                years_to_invest
            )
            if required_monthly_savings is not None:
                st.success(f"🎉 You need to save ZAR {required_monthly_savings:,.2f} per month to reach your goal of ZAR {savings_goal:,.2f} by age {retirement_age}. 🎉")
            else:
                st.error("It is not possible to reach your savings goal with the given parameters.")

def calculate_future_value(initial_investment, monthly_investment, annual_increase_rate, annual_return_rate, years):
    total_months = years * 12
    monthly_return_rate = annual_return_rate / 12
    monthly_increase_rate = (1 + annual_increase_rate) ** (1 / 12) - 1  # Convert annual increase rate to monthly

    total_value = initial_investment
    investment_values = []  # For plotting

    for month in range(1, total_months + 1):
        total_value *= (1 + monthly_return_rate)
        total_value += monthly_investment
        investment_values.append(total_value)

        # Increase monthly investment
        monthly_investment *= (1 + monthly_increase_rate)

    return total_value, investment_values

def calculate_required_monthly_savings(initial_investment, savings_goal, annual_increase_rate, annual_return_rate, years):
    total_months = years * 12
    monthly_return_rate = annual_return_rate / 12
    monthly_increase_rate = (1 + annual_increase_rate) ** (1 / 12) - 1  # Convert annual increase rate to monthly

    # Initialize variables
    low = 0.0
    high = savings_goal
    epsilon = 0.01  # Precision of the result
    max_iterations = 1000
    iteration = 0
    required_monthly_savings = None

    while low <= high and iteration < max_iterations:
        iteration += 1
        guess = (low + high) / 2
        total_value = initial_investment
        monthly_investment = guess

        for month in range(1, total_months + 1):
            total_value *= (1 + monthly_return_rate)
            total_value += monthly_investment
            # Increase monthly investment
            monthly_investment *= (1 + monthly_increase_rate)

        if abs(total_value - savings_goal) <= epsilon:
            required_monthly_savings = guess
            break
        elif total_value < savings_goal:
            low = guess
        else:
            high = guess

    return required_monthly_savings

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
    # Sidebar components
    st.sidebar.image("assets/image2.webp", use_container_width=True)
    st.sidebar.title("Select Your Calculator")
    st.sidebar.markdown("---")  # Horizontal separator
    app_mode = st.sidebar.radio("Choose Option:", ["💰 Investment Calculator", "📈 Inflation Calculator"])
    st.sidebar.markdown("---")
    st.sidebar.markdown("Built by msr")

    # Main content
    if app_mode == "💰 Investment Calculator":
        investment_calculator()
    elif app_mode == "📈 Inflation Calculator":
        inflation_calculator()

if __name__ == "__main__":
    main()

st.download_button(
    label="Download Results",
    data=results_dataframe.to_csv(index=False),
    file_name="investment_results.csv",
    mime="text/csv"
)

