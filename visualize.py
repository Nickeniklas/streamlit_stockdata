# Streamlit Data Visualization
import streamlit as st
import plotly.express as px  
import plotly.graph_objects as go
import pandas as pd  
import json
import glob
import os

# Page setup
st.set_page_config(page_title="Stocks and News", page_icon=":bar_chart:", layout="wide")  # page configuration

st.title(" :bar_chart: Stocks and News")  # title of the web page
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)  

# Find all stock files dynamically (assuming 'stockdata/stockdata_XXX.csv' format)
stock_files = glob.glob('stockdata/stockdata_*.csv')
# Extract ticker names from filenames
tickers = [f.split('_')[-1].replace('.csv', '') for f in stock_files]

# select ticker dropdown
selected_ticker = st.selectbox("Select Stock Ticker", tickers)

# load selected ticker data
file_path = f'stockdata/stockdata_{selected_ticker}.csv'
df = pd.read_csv(file_path)
df['datetime'] = pd.to_datetime(df['datetime'])

# STOCK DATA TABLE
st.subheader(f"Table: {selected_ticker}")
st.dataframe(df, use_container_width=True) 

# STOCK DATA GRAPH
# filter slider element: number of days to show
days = st.slider("How many past days to show", min_value=1, max_value=90, value=30)

# Moving Averages
df["MA10"] = df["close"].rolling(window=10).mean()
df["MA50"] = df["close"].rolling(window=50).mean()

# Filter to only show rows from the last N days
cutoff = df['datetime'].max() - pd.Timedelta(days=days)
df_filtered = df[df['datetime'] >= cutoff]

# Plotly chart
fig = go.Figure() # Create base figure

# Add traces for each series
# 1. Main close line with volume in hover
fig_close = px.line(
    df_filtered,
    x='datetime',
    y='close',
    hover_data=['volume'],
    title=f'Closing Prices for {selected_ticker}',
    labels={'close': 'Price (€)', 'datetime': 'Date'}
)
fig.add_trace(fig_close.data[0])

# 2. MA10 line (no volume in hover)
fig_ma10 = px.line(
    df_filtered,
    x='datetime',
    y='MA10',
    labels={'MA10': 'MA10'}
)
fig_ma10.update_traces(line=dict(color='red'), name='MA10')
fig.add_trace(fig_ma10.data[0])

# 3. MA50 line (no volume in hover)
fig_ma50 = px.line(
    df_filtered,
    x='datetime',
    y='MA50',
    labels={'MA50': 'MA50'}
)
fig_ma50.update_traces(line=dict(color='purple'), name='MA50')
fig.add_trace(fig_ma50.data[0])

fig.update_layout(title=f'{selected_ticker} Price with Moving Averages')

st.subheader(f"Graph: {selected_ticker} Line Chart with Moving Averages")
st.plotly_chart(fig, use_container_width=True) # Display the Plotly chart 

# GENERAL NEWS
# List all news JSON files like news_*.json
all_news_files = glob.glob("news/news_*.json")
all_news_data = []
# and add all news data to a list
for file_path in all_news_files:
    with open(file_path, "r", encoding="utf-8") as file:
        news_items = json.load(file)    
        all_news_data.extend(news_items)  

st.header(" :newspaper: News")

# the news
try: 
    for article in all_news_data: # Loop through and display each article
        st.subheader(article['headline'])
        st.write(article['summary'])
        st.write(f"**keyword: {article['keyword']}**")
        st.markdown(f"**Source:** {article['source']} — {article['url']}  ") # TBA: | **Date:** {article['date']}
        st.markdown('---')
except KeyError as e:
    st.error(f"Error displaying news articles: {e}")
    st.write("Please ensure the news data is correctly formatted and contains the expected fields.")