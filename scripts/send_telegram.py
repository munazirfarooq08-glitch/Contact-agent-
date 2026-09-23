import os
import json
import urllib.request
import urllib.parse

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }).encode()
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req) as resp:
        print(resp.read().decode())

def main():
    with open("dashboard/data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    my_handle = data["my_handle"]
    accounts = data["accounts"]
    my_posts = accounts.get(my_handle, [])

    my_avg_likes = round(sum(p.get("likes", 0) for p in my_posts) / len(my_posts)) if my_posts else 0

    competitors = {h: p for h, p in accounts.items() if h != my_handle}
    all_competitor_posts = []
    for h, posts in competitors.items():
        for p in posts:
            all_competitor_posts.append({**p, "handle": h})
    all_competitor_posts.sort(key=lambda p: p.get("likes", 0), reverse=True)
    top = all_competitor_posts[0] if all_competitor_posts else None

    lines = [
        "<b>📊 Content Desk — Daily Report</b>",
        "",
        f"Your avg likes/post: <b>{my_avg_likes}</b>",
        f"Posts tracked: {len(my_posts)}",
        "",
    ]

    if top:
        caption = (top.get("caption") or "")[:120]
        lines.append(f"🔥 Top competitor post right now: @{top['handle']} ({top.get('likes',0)} likes)")
        lines.append(f"\"{caption}\"")
        lines.append("")

    lines.append("Full dashboard: https://munazirfarooq08-glitch.github.io/Contact-agent-/dashboard/")

    send_message("\n".join(lines))

if __name__ == "__main__":
    main()
