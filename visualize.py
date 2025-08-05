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
st.title(" 📊 Stocks and News")  # title of the web page
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
df = df.sort_values('datetime', ascending=True).reset_index(drop=True)

# filter slider element: number of days to show
days = st.slider("How many past days to show", min_value=1, max_value=120, value=30)
# Moving Averages
df["MA10"] = df["close"].rolling(window=10).mean()
df["MA50"] = df["close"].rolling(window=50).mean()
# Filter by days
cutoff = df['datetime'].max() - pd.Timedelta(days=days)
df_filtered = df[df['datetime'] >= cutoff].copy()

# Plotly chart
fig = go.Figure() # GO base figure
# Calculate price change and percentage change
change_abs = df_filtered['close'].iloc[-1] - df_filtered['close'].iloc[0]
change_pct = (change_abs / df_filtered['close'].iloc[0]) * 100
# STOCK DATA GRAPH
# 1. Main close line with volume in hover
fig_close = px.line(
    df_filtered,
    x='datetime',
    y='close',
    hover_data=['volume'],
    title=f'Closing Prices for {selected_ticker}',
    labels={'close': 'Price (€)', 'datetime': 'Date'}
)
line_color = 'green' if change_abs > 0 else 'red'
fig_close.update_traces(line=dict(color=line_color), name='Close Price', showlegend=True)
fig.add_trace(fig_close.data[0])
# 2. MA10 line (no volume in hover)
fig_ma10 = px.line(
    df_filtered,
    x='datetime',
    y='MA10',
    labels={'MA10': 'MA10'}
)
fig_ma10.update_traces(line=dict(color='blue', dash='dot'), name='MA10', showlegend=True)
fig.add_trace(fig_ma10.data[0])
# 3. MA50 line (no volume in hover)
fig_ma50 = px.line(
    df_filtered,
    x='datetime',
    y='MA50',
    labels={'MA50': 'MA50'}
)
fig_ma50.update_traces(line=dict(color='purple', dash='dot'), name='MA50', showlegend=True)
fig.add_trace(fig_ma50.data[0])
# Add legends, axis titles and title
fig.update_layout(
    title=f'{selected_ticker} Price with Moving Averages', 
    legend_title='Legend',
    xaxis_title='Date',
    yaxis_title='Price (€)',
    )
# display change in price and percentage
st.metric(
    label=f"{selected_ticker}",
    value=f"{df_filtered['close'].iloc[-1]:.2f} €",
    delta=f"{change_pct:.2f}%"
)
# Display the Plotly chart 
st.plotly_chart(fig, use_container_width=True) 

# STOCK DATA TABLE
with st.expander(f" 📋 Table: {selected_ticker}", expanded=False):
    st.dataframe(df_filtered, height=400, use_container_width=True)

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
        st.write(f"**Date**: {article['datetime']} | **keyword:** {article['keyword']}")
        st.markdown(f"**Source:** {article['source']} — {article['url']}  ") # TBA: | **Date:** {article['date']}
        st.markdown('---')
except KeyError as e:
    st.error(f"Error displaying news articles: {e}")
    st.write("Please ensure the news data is correctly formatted and contains the expected fields.")