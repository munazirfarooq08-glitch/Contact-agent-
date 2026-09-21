import os
import json
from datetime import datetime, timezone
from apify_client import ApifyClient

APIFY_TOKEN = os.environ["APIFY_API_TOKEN"]
MY_HANDLE = os.environ["MY_INSTAGRAM_HANDLE"].strip()
COMPETITORS = [h.strip() for h in os.environ["COMPETITOR_HANDLES"].split(",") if h.strip()]

RESULTS_LIMIT = 30

client = ApifyClient(APIFY_TOKEN)

def fetch_posts(handle):
    run_input = {
        "directUrls": [f"https://www.instagram.com/{handle}/"],
        "resultsType": "posts",
        "resultsLimit": RESULTS_LIMIT,
    }
    run = client.actor("apify/instagram-scraper").call(run_input=run_input)
    dataset_id = run["defaultDatasetId"] if isinstance(run, dict) else run.default_dataset_id
    posts = []
    for item in client.dataset(dataset_id).iterate_items():
        posts.append({
            "caption": item.get("caption", ""),
            "likes": item.get("likesCount", 0),
            "comments": item.get("commentsCount", 0),
            "timestamp": item.get("timestamp", ""),
            "url": item.get("url", ""),
            "type": item.get("type", ""),
        })
    return posts

def main():
    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "my_handle": MY_HANDLE,
        "accounts": {}
    }

    print(f"Pulling data for my account: {MY_HANDLE}")
    data["accounts"][MY_HANDLE] = fetch_posts(MY_HANDLE)

    for handle in COMPETITORS:
        print(f"Pulling data for competitor: {handle}")
        data["accounts"][handle] = fetch_posts(handle)

    os.makedirs("dashboard", exist_ok=True)
    with open("dashboard/data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Saved to dashboard/data.json")

if __name__ == "__main__":
    main()
