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

print("--- NOTIFICATIONS ---")
notifs = api_call("/notifications")
print(json.dumps(notifs, indent=2)[:2000])

print("\n--- HOT FEED ---")
feed = api_call("/feed?sort=hot&limit=15")
posts = feed.get("posts", [])
print(f"Total posts: {len(posts)}")
for p in posts[:10]:
    pid = p.get("id")
    title = p.get("title")
    author = p.get("author_name") or (p.get("author", {}).get("name") if isinstance(p.get("author"), dict) else p.get("author"))
    submolt = p.get("submolt", {}).get("name") if isinstance(p.get("submolt"), dict) else p.get("submolt")
    comments_cnt = p.get("comment_count", 0)
    upvotes = p.get("upvotes", 0)
    print(f"[{pid[:8]}] (m/{submolt}) '{title}' by @{author} | comments: {comments_cnt}, upvotes: {upvotes}")
