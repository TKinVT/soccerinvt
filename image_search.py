import os
import requests
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("BING_KEY")
url = "https://api.bing.microsoft.com/v7.0/images/search"
headers = {"Ocp-Apim-Subscription-Key": key}

def image_search(search_term, freshness="week", count=5):
    params = {"q": search_term, "freshness": freshness, "count": count}
    r = requests.get(url, headers=headers, params=params)
    if r.ok:
        results = r.json()['value']
        return [x['contentUrl'] for x in results]
    else:
        return None
