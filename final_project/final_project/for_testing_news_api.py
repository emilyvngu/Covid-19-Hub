import json
import pandas as pd

# JSON string (unchanged)
json_string = '''{
    "status": "ok",
    "total_hits": 10000,
    "page": 1,
    "total_pages": 200,
    "page_size": 50,
    "articles": [
        {
            "summary": "ROTSELAAR — A 103-year-old Belgian doctor is walking a marathon around his garden in daily stages to raise money for research into the new coronavirus.",
            "country": "CA",
            "clean_url": "canoe.com",
            "author": "Reuters",
            "rights": null,
            "link": "https://canoe.com/news/world/belgian-aged-103-walking-marathon-to-raise-funds-for-covid-19-research",
            "rank": "9301",
            "topic": "NA",
            "language": "en",
            "title": "Belgian, 103, walking marathon to raise funds for COVID-19 research",
            "published_date": "2020-06-09 16:24:54",
            "_id": "6a7b63a5fb2284398bc1461af6ace3b0",
            "_score": 3.0822992
        }
    ],
    "user_input": {
        "q": "covid",
        "search_in": "title_summary_en",
        "lang": "en",
        "country": null,
        "from": "2020-06-01 00:00:00",
        "to": null,
        "ranked_only": "True",
        "from_rank": null,
        "to_rank": null,
        "sort_by": "date",
        "page": 1,
        "size": 50,
        "sources": null,
        "not_sources": [
            "dailymail.co.uk"
        ],
        "topic": null
    }
}'''

# Validate JSON string format
try:
    print("Validating JSON string...")
    json_data = json.loads(json_string)
    print("JSON is valid. Parsing now...")
except json.JSONDecodeError as e:
    print(f"JSON Decode Error: {e}")
    exit()

# Extract articles list
articles = json_data.get("articles", [])
if not articles:
    print("No articles found in JSON.")
    exit()

# Convert to a DataFrame
try:
    df = pd.DataFrame(articles)
    print("DataFrame created successfully!")
    print(df.head())
except Exception as e:
    print(f"Error converting articles to DataFrame: {e}")
