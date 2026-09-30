import sys, os, subprocess, json

PROXY = "127.0.0.1:10808"
API_KEY = "moltbook_sk__pOoz65X3V8P6mgBJzj0jfemKjZIdZ0s"
BASE_URL = "https://www.moltbook.com/api/v1"

def api_call(endpoint):
    url = f"{BASE_URL}{endpoint}" if endpoint.startswith("/") else f"{BASE_URL}/{endpoint}"
    cmd = [
        "curl", "-s", "--socks5-hostname", PROXY,
        url,
        "-H", f"Authorization: Bearer {API_KEY}",
        "-H", "User-Agent: Moltbook-Agent/1.0"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    try:
        return json.loads(res.stdout)
    except Exception:
        return {"raw": res.stdout[:500]}

print("=== HOT FEED ===")
feed = api_call("/feed?sort=hot&limit=15")
posts = feed.get("posts", [])
print(f"Retrieved {len(posts)} posts from hot feed:")
for p in posts:
    print(f"ID: {p.get('id')} | submolt: {p.get('submolt')} | author: {p.get('author_name') or p.get('author',{}).get('name')} | upvotes: {p.get('upvotes_count', p.get('score'))} | comments: {p.get('comments_count')} | title: {p.get('title')[:60]}")
