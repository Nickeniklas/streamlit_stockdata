import finnhub
import json
from dotenv import load_dotenv
import os
from datetime import datetime

# get api key from .env file
load_dotenv()
api_key = os.getenv('FINNHUB_API_KEY')
if not api_key:
    raise ValueError("No API key found. Please set FINNHUB_API_KEY in .env")

finnhub_client = finnhub.Client(api_key=api_key)

# fetch news 
marketNewsData = finnhub_client.general_news('general', min_id=0)

# set keyword for news
news_keywords = ["Trump", "Apple", "NVIDIA", "Oracle", "Microsoft"]

# loop through all keywords and export filtered news
for keyword in news_keywords:
    # filter with keyword 
    filtered = [item for item in marketNewsData if keyword in item["headline"]]
    # message if no news found
    if not filtered:
        print(f"No news headlines found mentioning {keyword}.")
    else:
        # Extract top 3 news with only wanted fields
        simplifiedNews = [
            {
                'headline': news['headline'],
                'summary': news['summary'],
                'source' : news['source'],
                'url': news['url'],
                'datetime' : datetime.fromtimestamp(news['datetime']).strftime('%d-%m-%y'),
                'keyword' : keyword
            }
            for news in filtered[:3] # top 3 articles only
        ] 

        # output folder and pathfile name
        folder = "news"
        os.makedirs(folder, exist_ok=True)  # Create the folder if it doesn't exist
        filepath = os.path.join(folder, f"news_{keyword}.json")
        # Save to a JSON file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(simplifiedNews, f, ensure_ascii=False, indent=2)

        # save message
        print(f"Saved top {keyword} news as '{filepath}'")
   