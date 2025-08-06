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

# default ticker selection
if "selected_ticker" not in st.session_state:
    st.session_state.selected_ticker = tickers[0]
# Dropdown for ticker selection
dropdown_choice = st.selectbox("Select Stock Ticker", tickers, index=tickers.index(st.session_state.selected_ticker))
with st.sidebar:
    dropdown_choice = st.selectbox("Select Stock Ticker", tickers, index=tickers.index(st.session_state.selected_ticker))
# Update session state if dropdown choice changes
if dropdown_choice != st.session_state.selected_ticker:
    st.session_state.selected_ticker = dropdown_choice

# days filter defualt 30 days
if "days" not in st.session_state:
    st.session_state.days = 30

# load selected ticker data
file_path = f'stockdata/stockdata_{st.session_state.selected_ticker}.csv'
df = pd.read_csv(file_path)
df['datetime'] = pd.to_datetime(df['datetime'])
df = df.sort_values('datetime', ascending=True).reset_index(drop=True)

# FILTER BUTTONS: number of days to show
filter_days = [(1, "1D"), (30, "1M"), (90, "3M"), (120, "4M")]   
filter_day_columns = st.sidebar.columns(len(filter_days))  # Create columns for buttons
# Create the buttons
with st.sidebar:
    for i, (days, label) in enumerate(filter_days):
        # Inject custom CSS
        st.markdown(f"""
            <style>
                .st-key-{label} button {{
                    width: 3rem;
                }}
            </style>
        """, unsafe_allow_html=True)
        with filter_day_columns[i]:
            # Button click sets selected days
            if st.button(label, key=f"{label}"):
                st.session_state.days = days # set days
                st.rerun()  # reflect change immediately

# FILTER SLIDER: number of days to show
st.session_state.days = st.slider("How many past days to show", min_value=1, max_value=120, value=st.session_state.days)

# Calculate Moving Averages
df["MA10"] = df["close"].rolling(window=10).mean()
df["MA50"] = df["close"].rolling(window=50).mean()

# DataFrame Filter by days
cutoff = df['datetime'].max() - pd.Timedelta(days=st.session_state.days)
df_filtered = df[df['datetime'] >= cutoff].copy()

# DISPLAY ALL TICKERS CHANGE
st.subheader("All Tickers Change")

# Make a horizontal layout with Streamlit columns
ticker_card_columns = st.columns(len(tickers))

for i, ticker in enumerate(tickers):
    # Load ticker data
    file_path = f'stockdata/stockdata_{ticker}.csv'
    df_ticker = pd.read_csv(file_path)
    df_ticker['datetime'] = pd.to_datetime(df_ticker['datetime'])
    df_ticker = df_ticker.sort_values('datetime', ascending=True).reset_index(drop=True)
    cutoff = df_ticker['datetime'].max() - pd.Timedelta(days=st.session_state.days)
    df_ticker_filtered = df_ticker[df_ticker['datetime'] >= cutoff].copy()

    # Calculate price change and percentage change
    change_abs = df_ticker_filtered['close'].iloc[-1] - df_ticker_filtered['close'].iloc[0]
    change_pct = (change_abs / df_ticker_filtered['close'].iloc[0]) * 100

    # Display ticker cards
    # Color background based on gain/loss
    bg_color = "#d4edda" if change_abs > 0 else "#f8d7da"
    text_color = "#155724" if change_abs > 0 else "#721c24"

    with ticker_card_columns[i]:
        button_label = f"{ticker}\n{change_abs:.2f} € ({change_pct:.2f}%)"
        # Inject custom CSS
        st.markdown(f"""
            <style>
                .st-key-{ticker} button {{
                    background-color: {bg_color};
                    color: {text_color};
                }}
            </style>
        """, unsafe_allow_html=True)
        # Button click sets selected ticker
        if st.button(button_label, key=f"{ticker}"):
            st.session_state.selected_ticker = ticker # set ticker
            st.rerun()  # reflect change immediately

# PLOTLY CHART
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
    title=f'Closing Prices for {st.session_state.selected_ticker}',
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
    title=f'{st.session_state.selected_ticker} Price with Moving Averages', 
    legend_title='Legend',
    xaxis_title='Date',
    yaxis_title='Price (€)',
    )
# display change in price and percentage
st.metric(
    label=f"{st.session_state.selected_ticker}",
    value=f"{df_filtered['close'].iloc[-1]:.2f} €",
    delta=f"{change_pct:.2f}%"
)
# Display the Plotly chart 
st.plotly_chart(fig, use_container_width=True) 

# STOCK DATA TABLE
with st.expander(f" 📋 Table: {st.session_state.selected_ticker}", expanded=False):
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