import finnhub
import json
from dotenv import load_dotenv
import os

# get api key from .env file
load_dotenv()
api_key = os.getenv('FINNHUB_API_KEY')
if not api_key:
    raise ValueError("No API key found. Please set FINNHUB_API_KEY in .env")

finnhub_client = finnhub.Client(api_key=api_key)

# fetch news 
marketNewsData = finnhub_client.general_news('general', min_id=0)

# filter with keyword "Trump"
filtered = [item for item in marketNewsData if "Trump" in item["headline"]]
# message if no news found
if not filtered:
    print("No news headlines found mentioning Trump.")
else:
    # Extract top 3 news with only wanted fields
    simplifiedNews = [
        {
            'headline': news['headline'],
            'summary': news['summary'],
            'url': news['url']
        }
        for news in filtered[:3]
    ] 

    # Save to a JSON file
    with open('filtered_news.json', 'w', encoding='utf-8') as f:
        json.dump(simplifiedNews, f, ensure_ascii=False, indent=2)

    # save message
    print("Saved top news to filtered_news.json")
   