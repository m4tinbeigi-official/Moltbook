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
    return json.loads(res.stdout)

feed = api_call("/feed?sort=hot&limit=5")
posts = feed.get("posts", [])
if posts:
    print("Post keys:", list(posts[0].keys()))
    print("Post author:", posts[0].get("author"))

notif3 = api_call("/posts/c89c7705-6aa5-456d-8308-13490b8cd09e/comments?sort=new&limit=25")
comments = notif3.get("comments", [])
print(f"\nComments count in c89c: {len(comments)}")
for c in comments:
    if c.get("id") == "4b36b84d-2775-40c7-8821-a8ada0dac324":
        print("FOUND NOTIF 3 COMMENT:")
        print(json.dumps(c, indent=2))
