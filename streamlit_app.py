import streamlit as st
import numpy as np
import pandas as pd

def calculate_fee(current_investment, annual_contribution, years, fee_percent, growth_percent):
    """Calculate the total amount and fee cost over a period with compound growth and return detailed yearly data."""
    data = []
    total_investment = current_investment
    total_fee_paid = 0
    fee_rate = fee_percent / 100
    growth_rate = growth_percent / 100

    for year in range(1, years + 1):
        growth = total_investment * growth_rate
        total_investment += growth
        annual_fee = total_investment * fee_rate
        total_fee_paid += annual_fee
        total_investment += annual_contribution - annual_fee
        data.append((year, total_investment, annual_fee, total_fee_paid))

    df = pd.DataFrame(data, columns=["Year", "Total Investment", "Annual Fee", "Total Fee Paid"])
    df["Total Investment"] = df["Total Investment"].apply(lambda x: f"${x:,.0f}")
    df["Annual Fee"] = df["Annual Fee"].apply(lambda x: f"${x:,.0f}")
    df["Total Fee Paid"] = df["Total Fee Paid"].apply(lambda x: f"${x:,.0f}")
    return df, total_investment, total_fee_paid

def main():
    st.title("Investment Fee Calculator")

    # Sidebar for input fields with defaults
    with st.sidebar:
        # Using text_input to allow formatted display
        current_investment_input = st.text_input("Current Investment Amount", value="25,000,000")
        # Convert formatted string to float
        try:
            current_investment = float(current_investment_input.replace(',', ''))
        except ValueError:
            st.error("Please enter a valid number for Current Investment Amount.")
            return
        
        annual_contribution = st.number_input("Annual Contribution", min_value=0.0, format="%.2f")
        years = st.slider("Number of Years Investing", min_value=1, max_value=60, value=50)
        fee_percent1 = st.number_input("Investment Fee 1 (%)", min_value=0.0, max_value=100.0, format="%.2f")
        fee_percent2 = st.number_input("Investment Fee 2 (%)", min_value=0.0, max_value=100.0, format="%.2f", value=0.75)
        growth_percent = st.number_input("Rate of Growth for Investments (%)", min_value=0.0, max_value=100.0, format="%.2f", value=5.0)
    
    # Calculate data
    df1, total_investment1, total_fee_paid1 = calculate_fee(current_investment, annual_contribution, years, fee_percent1, growth_percent)
    df2, total_investment2, total_fee_paid2 = calculate_fee(current_investment, annual_contribution, years, fee_percent2, growth_percent)
    difference_in_fee_paid = total_investment1 - total_investment2

    # Display results
    st.write(f"After {years} years, the total investment with Fee 1 will be ${total_investment1:,.0f}.")
    st.write(f"After {years} years, the total investment with Fee 2 will be ${total_investment2:,.0f}.")
    st.write(f"Difference in investment due to fees: ${difference_in_fee_paid:,.0f}.")

    # Prepare data for line chart
    chart_data = pd.DataFrame({
        "Fee 1": df1['Total Investment'].replace('[\$,]', '', regex=True).astype(float),
        "Fee 2": df2['Total Investment'].replace('[\$,]', '', regex=True).astype(float),
    }, index=df1['Year'])

    # Plotting the growth comparison using st.line_chart
    st.line_chart(chart_data)

    # Display tables
    st.write("Yearly details for Fee 1:")
    st.dataframe(df1)
    st.write("Yearly details for Fee 2:")
    st.dataframe(df2)

if __name__ == "__main__":
    main()
