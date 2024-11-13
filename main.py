# Investment, Inflation Calculator, and Live Market Rates Web App
import streamlit as st
import numpy as np
import datetime
import pandas as pd
import requests
import yfinance as yf
from PIL import Image  # Import PIL for image handling
import os

def main():
    # Set the page config for a better layout and title
    st.set_page_config(
        page_title="Financial Tools",
        page_icon="💹",
        layout="wide",
        # initial_sidebar_state="collapsed",
    )
    
    # Load and display the image in the sidebar
    st.sidebar.title("Welcome to Financial Tools")
    image_path = os.path.join('assets', 'image2.webp')  # Adjust the path as needed
    image = Image.open(image_path)
    st.sidebar.image(image, use_column_width=True)

    # Add a brief description or tagline
    st.sidebar.markdown(
        """
        **Empower your financial decisions with our comprehensive suite of tools.**
        """
    )
    
    # Navigation options with icons
    options = ["📈 Investment Calculator", "💰 Inflation Calculator", "📊 Live Market Rates"]
    choice = st.sidebar.radio("Navigate", options)
    
    if choice == "📈 Investment Calculator":
        investment_calculator()
    elif choice == "💰 Inflation Calculator":
        inflation_calculator()
    elif choice == "📊 Live Market Rates":
        live_rates()

def investment_calculator():
    st.title("📈 Investment Calculator")
    st.write("---")  # Horizontal separator

    # Selection option with tabs for better UX
    tabs = st.tabs(["Future Value at Retirement", "Monthly Savings to Reach Goal"])
    with tabs[0]:
        future_value_calculator()
    with tabs[1]:
        required_savings_calculator()

def future_value_calculator():
    st.header("Future Value at Retirement")
    st.write("Calculate how much your investments will grow over time.")

    # Inputs
    current_age = st.number_input("Current Age", min_value=0, value=25)
    retirement_age = st.number_input("Retirement Age", min_value=current_age + 1, value=65)
    years_to_invest = retirement_age - current_age

    initial_investment_amount = st.number_input("Initial Investment Amount (ZAR)", min_value=0.0, value=50000.0, step=1000.0, format="%.2f")
    initial_monthly_investment = st.number_input("Initial Monthly Investment (ZAR)", min_value=0.0, value=5000.0, step=100.0, format="%.2f")
    annual_increase_rate = st.slider("Annual Increase Rate of Monthly Investment (%)", min_value=0.0, max_value=20.0, value=10.0, step=0.1) / 100
    annual_return_rate = st.slider("Annual Return Rate (%)", min_value=0.0, max_value=20.0, value=9.0, step=0.1) / 100

    if st.button("Calculate Future Value"):
        total_value, investment_values = calculate_future_value(
            initial_investment_amount,
            initial_monthly_investment,
            annual_increase_rate,
            annual_return_rate,
            years_to_invest
        )
        st.success(f"At age {retirement_age}, you will have: **ZAR {total_value:,.2f}**")
        st.balloons()

        # Plot the investment growth over time
        plot_investment_growth(investment_values, years_to_invest)

def required_savings_calculator():
    st.header("Required Monthly Savings to Reach Goal")
    st.write("Determine how much you need to save monthly to reach your retirement goal.")

    # Inputs
    current_age = st.number_input("Current Age", min_value=0, value=25, key='current_age_req')
    retirement_age = st.number_input("Retirement Age", min_value=current_age + 1, value=65, key='retirement_age_req')
    years_to_invest = retirement_age - current_age

    initial_investment_amount = st.number_input("Initial Investment Amount (ZAR)", min_value=0.0, value=50000.0, step=1000.0, format="%.2f", key='initial_investment_req')
    savings_goal = st.number_input("Savings Goal at Retirement (ZAR)", min_value=0.0, value=6000000.0, step=1000.0, format="%.2f")
    annual_increase_rate = st.slider("Annual Increase Rate of Monthly Savings (%)", min_value=0.0, max_value=20.0, value=0.0, step=0.1) / 100
    annual_return_rate = st.slider("Annual Return Rate (%)", min_value=0.0, max_value=20.0, value=9.0, step=0.1, key='return_rate_req') / 100

    if st.button("Calculate Required Monthly Savings"):
        required_monthly_savings = calculate_required_monthly_savings(
            initial_investment_amount,
            savings_goal,
            annual_increase_rate,
            annual_return_rate,
            years_to_invest
        )
        if required_monthly_savings is not None:
            st.success(f"You need to save **ZAR {required_monthly_savings:,.2f}** per month to reach your goal of **ZAR {savings_goal:,.2f}** by age {retirement_age}.")
        else:
            st.error("It is not possible to reach your savings goal with the given parameters.")

def calculate_future_value(initial_investment, monthly_investment, annual_increase_rate, annual_return_rate, years):
    total_months = years * 12
    monthly_return_rate = (1 + annual_return_rate) ** (1/12) - 1
    monthly_increase_rate = (1 + annual_increase_rate) ** (1 / 12) - 1

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
    monthly_return_rate = (1 + annual_return_rate) ** (1/12) - 1
    monthly_increase_rate = (1 + annual_increase_rate) ** (1 / 12) - 1

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

def plot_investment_growth(investment_values, years):
    df = pd.DataFrame({
        'Month': range(1, years * 12 + 1),
        'Investment Value': investment_values
    })
    st.line_chart(df.set_index('Month'), use_container_width=True)
    st.caption("Investment Growth Over Time")

def inflation_calculator():
    st.title("💰 Inflation Calculator")
    st.write("---")  # Horizontal separator
    st.write("Adjust future amounts for inflation to understand their present-day value.")

    # Input fields for inflation parameters
    amount = st.number_input("Enter the Future Amount of Money (ZAR)", min_value=0.0, value=55000000.0, step=1000.0, format="%.2f")
    target_year = st.number_input("Enter the Future Year", min_value=datetime.datetime.now().year + 1, value=2055, step=1)
    inflation_rate = st.slider("Annual Inflation Rate (%)", min_value=0.0, max_value=10.0, value=3.0, step=0.1)

    if st.button("Calculate Inflation Adjustment"):
        current_year = datetime.datetime.now().year
        years_difference = target_year - current_year
        inflation_rate_decimal = inflation_rate / 100
        # Adjust the amount for inflation
        adjusted_value = amount / ((1 + inflation_rate_decimal) ** years_difference)
        st.success(f"The amount of **ZAR {amount:,.2f}** in {target_year} will be worth **ZAR {adjusted_value:,.2f}** in {current_year}, adjusted for inflation.")

def live_rates():
    st.title("📊 Live Market Rates")
    st.write("---")  # Horizontal separator
    st.write("Stay updated with the latest market rates for cryptocurrencies and stocks.")

    try:
        # Cryptocurrency
        st.subheader("Cryptocurrency")
        btc_url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        btc_params = {"vs_currency": "usd", "days": "30"}
        btc_data = requests.get(btc_url, params=btc_params).json()
        btc_prices = [price[1] for price in btc_data["prices"]]
        btc_dates = [price[0] for price in btc_data["prices"]]
        btc_df = pd.DataFrame({"Date": pd.to_datetime(btc_dates, unit="ms"), "Price (USD)": btc_prices})

        # Display latest price and historical chart
        st.metric("Bitcoin (BTC)", f"${btc_prices[-1]:,.2f}")
        st.line_chart(btc_df.set_index("Date")["Price (USD)"], use_container_width=True)

        # Stocks
        st.subheader("Stocks")
        stocks = {
            "MicroStrategy (MSTR)": "MSTR",
            "S&P 500 (^GSPC)": "^GSPC",
            "Nvidia (NVDA)": "NVDA"
        }

        for stock_name, ticker in stocks.items():
            stock = yf.Ticker(ticker)
            stock_data = stock.history(period="1mo")  # Fetch 1-month historical data
            latest_price = stock_data["Close"].iloc[-1]

            # Display latest price and historical chart
            st.metric(stock_name, f"${latest_price:,.2f}")
            st.line_chart(stock_data["Close"], use_container_width=True)

    except Exception as e:
        st.error("Unable to fetch live rates at the moment. Please try again later.")

if __name__ == "__main__":
    main()
