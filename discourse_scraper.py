
import requests
import pandas as pd
from datetime import datetime

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"
CATEGORY_URL = f"{BASE_URL}/c/courses/tds-kb/34.json"

def fetch_topics():
    response = requests.get(CATEGORY_URL)
    topics = response.json()['topic_list']['topics']
    return topics

def fetch_topic_details(topic_id):
    url = f"{BASE_URL}/t/{topic_id}.json"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

def scrape_discourse(start_date, end_date):
    topics = fetch_topics()
    results = []

    for topic in topics:
        created_at = datetime.strptime(topic['created_at'][:10], "%Y-%m-%d")
        if start_date <= created_at <= end_date:
            details = fetch_topic_details(topic['id'])
            if details:
                first_post = details['post_stream']['posts'][0]
                results.append({
                    'Title': topic['title'],
                    'URL': f"{BASE_URL}/t/{topic['slug']}/{topic['id']}",
                    'Created': topic['created_at'],
                    'Content': first_post['cooked']
                })

    return pd.DataFrame(results)

# Example run
if __name__ == "__main__":
    start = datetime(2024, 12, 1)
    end = datetime(2025, 6, 1)
    df = scrape_discourse(start, end)
    df.to_csv("discourse_tds_scraped.csv", index=False)
    print("Done scraping!")
