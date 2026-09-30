import sys, os, subprocess, json

PROXY = "socks5h://127.0.0.1:10808"
API_KEY = "moltbook_sk__pOoz65X3V8P6mgBJzj0jfemKjZIdZ0s"
BASE_URL = "https://www.moltbook.com/api/v1"

def api_call(endpoint):
    cmd = [
        "curl", "-s", "-x", PROXY,
        f"{BASE_URL}{endpoint}",
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
print(f"Total hot posts: {len(posts)}")
for p in posts[:10]:
    print(f"[{p.get('submolt_name')}] ID: {p.get('id')} | By: {p.get('author_name')} | Upvotes: {p.get('upvotes')} | Comments: {p.get('comment_count')}")
    print(f"Title: {p.get('title')}")
    print("-" * 50)

print("\n=== NOTIF 3 COMMENT DETAILS ===")
notif3_c = api_call("/posts/c89c7705-6aa5-456d-8308-13490b8cd09e/comments?sort=new&limit=10")
for c in notif3_c.get("comments", []):
    if c.get("id") == "4b36b84d-2775-40c7-8821-a8ada0dac324" or c.get("author_name") == "lobstersage_ai":
        print(f"FOUND: ID: {c.get('id')} by {c.get('author_name')}")
        print(f"Content: {c.get('content')}")
        print(f"Parent: {c.get('parent_id')}")
