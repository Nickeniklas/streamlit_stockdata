# Streamlit Data Visualization
import streamlit as st
import plotly.express as px  
import pandas as pd  

# file name
file = "stockdata.csv"

# Reading the CSV file into a DataFrame
df = pd.read_csv(file, header=0, encoding='unicode_escape')

# set title
title = file.removesuffix(".csv")

# Page setup
st.set_page_config(page_title=f"{title} Visualization", page_icon=":bar_chart:", layout="wide")  # page configuration

st.title(f" :bar_chart: Visualization of {title}")  # title of the web page
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)  # Adding custom CSS to the page

st.write(f"{title} plotted as a line chart.")

# Displaying the DataFrame
st.write(df)  

st.line_chart(df['Close']) # Creating a line chart using Plotly Express