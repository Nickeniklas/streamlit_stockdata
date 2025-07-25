# Streamlit Data Visualization

Dynamic Visualization with Streamlit

TwelveData, Finnhub, Streamlit

## 1. Create virutal environment and activate it
Command to create conda virtual environment:
```
conda create --name <my-env>
```
Command to activate virtual environment:
```
conda activate <my-env>
```

## 2. Download required packages
```
pip install -r requirements.txt
```
If already installed(also update existing packages):
```
pip install --upgrade -r requirements.txt
```

## 3. Create .env for news api key and add it to .gitignore 
**.env** file:
```
FINNHUB_API_KEY=your_actual_api_key
```
**.gitignore** file:
```
.env
```

## 4. Run scripts
Command to run Fetch News Data:
```
python fetch_news.py
```

Command to run Fetch Stock Data:
```
python fetch_stockdata.py
```

Command to run Visualization in browser:
```
streamlit run visualize.py
```
