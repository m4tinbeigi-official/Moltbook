import sys
import os
import subprocess
import json

API_KEY = "moltbook_sk__pOoz65X3V8P6mgBJzj0jfemKjZIdZ0s"
BASE_URL = "https://www.moltbook.com/api/v1"
PROXY = "socks5h://127.0.0.1:10808"

def api_call(endpoint):
    url = f"{BASE_URL}{endpoint}" if endpoint.startswith("/") else f"{BASE_URL}/{endpoint}"
    cmd = [
        "curl", "-s", "-x", PROXY,
        url,
        "-H", f"Authorization: Bearer {API_KEY}",
        "-H", "User-Agent: Moltbook-Agent/1.0"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
    try:
        return json.loads(res.stdout)
    except Exception as e:
        return {"raw": res.stdout, "err": str(e)}

if __name__ == "__main__":
    home = api_call("/home")
    print("HOME:", json.dumps(home, indent=2))
    notifs = api_call("/notifications?limit=10")
    print("NOTIFS:", json.dumps(notifs, indent=2))
    feed = api_call("/feed?sort=hot&limit=15")
    posts = feed.get("posts", [])
    print(f"FEED_HOT_COUNT: {len(posts)}")
    for i, p in enumerate(posts[:10]):
        print(f"[{i+1}] id={p.get('id')} sub={p.get('submolt')} comments={p.get('comment_count')} upvotes={p.get('upvotes')} author={p.get('author',{}).get('name')} title={p.get('title')}")
