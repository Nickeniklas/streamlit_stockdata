# Streamlit Data Visualization
import streamlit as st
import plotly.express as px  
import pandas as pd  
import json
import glob

# Stock Data file name
file_path = "stockdata.csv"

# Reading the CSV file into a DataFrame
df = pd.read_csv(file_path, header=0, encoding='unicode_escape')

# set title
title = file_path.removesuffix(".csv")

# Page setup
st.set_page_config(page_title=f"{title} Visualization", page_icon=":bar_chart:", layout="wide")  # page configuration

st.title(f" :bar_chart: Visualization of {title}")  # title of the web page
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)  # Adding custom CSS to the page

st.write(f"{title} plotted as a line chart.")

# Displaying the DataFrame
st.write(df)  

st.line_chart(df['Close']) # Creating a line chart using Plotly Express

# GENERAL NEWS

# List all news JSON files like news_*.json
all_news_files = glob.glob("news_*.json")
all_news_data = []

for file_path in all_news_files:
    with open(file_path, "r", encoding="utf-8") as file:
        news_items = json.load(file)    
        all_news_data.extend(news_items)  

st.header(" :newspaper: News")

# the news
for article in all_news_data: # Loop through and display each article
    st.subheader(article['headline'])
    st.write(article['summary'])
    st.write(f'**keyword: {article['keyword']}**')
    st.markdown(f"**Source:** {article['source']} — {article['url']}  ") # TBA: | **Date:** {article['date']}
    st.markdown('---')