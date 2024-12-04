import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from petroleumpriceprediction.config import load_config
import pickle

# Set up the page title
st.set_page_config(page_title="Oil Price Prediction Dashboard", layout="wide")

# Title and description
st.title("Brent Oil Price Prediction")
st.markdown("""
This interactive dashboard is designed to assist in analyzing Brent oil prices, 
providing historical insights, global consumption trends, and forecasts to aid decision-making.  
Select the number of days to forecast future prices and see the results visually.
""")

# **Loading Files**
config = load_config("config.yaml")
dataset_filepath = config["data"]["dataset_filepath"]
consumption_filepath = config["data"]["consumption_filepath"]
opec_filepath = config["data"]["opec_filepath"]
model_filepath = config["model"]["path"]

# Load the datasets
df_brent = pd.read_csv(dataset_filepath)
df_consumption = pd.read_csv(consumption_filepath)
df_opec = pd.read_csv(opec_filepath)

# Ensure the date columns are in datetime format
df_brent['date'] = pd.to_datetime(df_brent['date'])
df_brent = df_brent.sort_values(by='date')

df_opec['date'] = pd.to_datetime(df_opec['date'])
df_opec = df_opec.sort_values(by='date')

# Load the SARIMAX model
with open(model_filepath, "rb") as f:
    sarimax = pickle.load(f)

# **Section 1: Historical Prices Chart and Summary Table**
st.subheader("Historical Brent Oil Prices")

# Create a detailed summary table
last_price = df_brent['price'].iloc[-1]
last_date = df_brent['date'].iloc[-1]
prev_price = df_brent['price'].iloc[-2]
price_one_year_ago = df_brent[df_brent['date'] == last_date - pd.Timedelta(days=365)]['price'].values[0] if len(df_brent[df_brent['date'] == last_date - pd.Timedelta(days=365)]) > 0 else None

summary_data = {
    "Metric": [
        "Last Date", 
        "Last Value", 
        "Previous Day Price", 
        "1-Day Change (%)", 
        "Price One Year Ago", 
        "1-Year Change (%)"
    ],
    "Value": [
        last_date.date(), 
        last_price, 
        prev_price, 
        f"{round(((last_price - prev_price) / prev_price) * 100, 2)}%", 
        price_one_year_ago if price_one_year_ago else "N/A", 
        f"{round(((last_price - price_one_year_ago) / price_one_year_ago) * 100, 2)}%" if price_one_year_ago else "N/A"
    ]
}

summary_table = pd.DataFrame(summary_data)

col1, col2 = st.columns(2)

with col1:
    # Add a year column to the dataframe
    df_brent['year'] = df_brent['date'].dt.year

    # Define a color palette for the years
    years = df_brent['year'].unique()
    colors = sns.color_palette("tab10", len(years))  # You can use other palettes available in seaborn
    color_map = {year: color for year, color in zip(years, colors)}

    # Create the plot with colors by year
    fig, ax = plt.subplots(figsize=(10, 5))
    for year in years:
        year_data = df_brent[df_brent['year'] == year]
        ax.plot(year_data['date'], year_data['price'], label=f"Year {year}", color=color_map[year])

    # Customize the chart
    ax.set_xlabel("Date")
    ax.set_ylabel("Price ($)")
    ax.legend(title="Year")
    st.pyplot(fig)

with col2:
    # Display the summary table
    st.write("**Recent Price Summary**")
    st.table(pd.DataFrame(summary_table))

# **Section 2: Price Comparison (OPEC vs Brent)**
st.subheader("Price Comparison: OPEC vs Brent")

col1, col2 = st.columns(2)

with col1:
    # OPEC vs Brent Chart
    merged_df = pd.merge(df_brent, df_opec, on='date', how='inner', suffixes=('_brent', '_opec'))
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(merged_df['date'], merged_df['price'], label="Brent Price", color="blue")
    ax.plot(merged_df['date'], merged_df['opec_price'], label="OPEC Price", color="orange")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price ($)")
    ax.legend()
    st.pyplot(fig)

with col2:
    # Explanation
    st.write("**Why Compare?**")
    st.markdown("""
    - Comparing Brent and OPEC prices helps understand the relationship between two key global benchmarks.  
    - Discrepancies or convergence in prices may reflect economic shocks, OPEC production decisions, or other global events.
    """)

# **Section 3: Global Oil Consumption**
st.subheader("Global Oil Consumption")

col1, col2 = st.columns(2)

with col1:
    # Global consumption chart with trend line
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x="year", y="consumption", data=df_consumption, ax=ax, palette="Blues_d")
    ax.set_xlabel("Year")
    ax.set_ylabel("Daily Consumption (Thousands of Barrels)")
    st.pyplot(fig)

with col2:
    st.write("**Global Consumption Trends**")
    st.markdown("""
    - Global oil consumption has shown a growth trend, reflected by the red trend line.  
    - This indicates a consistent increase in demand for oil, with potential implications for prices and production in the future.
    """)

# **Section 4: Forecasting**
st.subheader("Future Price Forecast")

# Select the number of days for the forecast
forecast_days = st.slider("Select the number of days for the forecast", min_value=1, max_value=7, step=1)

# Create forecast using the model
if forecast_days > 0:
    last_date = df_brent['date'].iloc[-1]
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_days, freq='D')
    future_exog = None  # If there are exogenous variables, include the corresponding future data here.
    
    forecast = sarimax.forecast(steps=forecast_days)

    # DataFrame with forecasted values
    forecast_df = pd.DataFrame({'date': future_dates, 'forecast_price': forecast})
    
    # Display the forecast table
    st.write(f"Forecast for the next {forecast_days} days:")
    st.write(forecast_df)

    # Filter the last month's historical data
    last_month_data = df_brent[df_brent['date'] >= (df_brent['date'].max() - pd.Timedelta(days=7))]

    # Forecast chart with historical data from the last month
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(last_month_data['date'], last_month_data['price'], label="Historical Brent Price", color="blue")
    ax.plot(forecast_df['date'], forecast_df['forecast_price'], label="Forecast", color="green", linestyle="--")
    ax.set_title(f"Future Price Forecast for the Next {forecast_days} Days")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price ($)")
    ax.legend()
    st.pyplot(fig)
