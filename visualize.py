# Streamlit Data Visualization
import streamlit as st
import plotly.express as px  
import pandas as pd  
import json
import glob
import os

# Stock Data file name
file_path = "stockdata/stockdata_AAPL.csv"

# Reading the CSV file into a DataFrame
df = pd.read_csv(file_path, header=0, encoding='unicode_escape')
df['datetime'] = pd.to_datetime(df['datetime'])  # if not already datetime
#df.set_index('datetime', inplace=True)
#print(df.head(10))

# file path of stock data
path = file_path.removesuffix(".csv")
ticker = path.split("_")[-1]

# Page setup
st.set_page_config(page_title="Stocks and News", page_icon=":bar_chart:", layout="wide")  # page configuration

st.title(" :bar_chart: Stocks and News")  # title of the web page
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)  # Adding custom CSS to the page

# STOCK DATA TABLE
st.subheader(f"Table: {ticker}")
st.dataframe(df, use_container_width=True) 

# STOCK DATA GRAPH
# filter slider element: number of days to show
days = st.slider("How many past days to show", min_value=1, max_value=90, value=30)

# Filter to only show rows from the last N days
cutoff = df['datetime'].max() - pd.Timedelta(days=days)
df_filtered = df[df['datetime'] >= cutoff]

# Plotly chart
fig = px.line(
    df_filtered,
    x='datetime',
    y='close',
    hover_data=['volume'],
    #color_discrete_sequence=['blue'],
    title=f'Closing Prices for {ticker}',
    labels={'close': 'Price (€)', 'datetime': 'Date'},
    template='seaborn'
)
fig.update_layout(
    #paper_bgcolor='white',
    #plot_bgcolor='white',
    #font_color='black'
)

st.subheader(f"Graph: {ticker} Closing Prices")
st.plotly_chart(fig)

#st.subheader("Close Price for AAPL")
#st.line_chart(df['close']) # line chart of the 'close' column

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
        st.write(f'**keyword: {article['keyword']}**')
        st.markdown(f"**Source:** {article['source']} — {article['url']}  ") # TBA: | **Date:** {article['date']}
        st.markdown('---')
except KeyError as e:
    st.error(f"Error displaying news articles: {e}")
    st.write("Please ensure the news data is correctly formatted and contains the expected fields.")