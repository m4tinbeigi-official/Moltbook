import subprocess, json

PROXY = "socks5h://127.0.0.1:10808"
API_KEY = "moltbook_sk__pOoz65X3V8P6mgBJzj0jfemKjZIdZ0s"

cmd = [
    "curl", "-s", "-x", PROXY,
    "https://www.moltbook.com/api/v1/feed?sort=hot&limit=15",
    "-H", f"Authorization: Bearer {API_KEY}",
    "-H", "User-Agent: Moltbook-Agent/1.0"
]
res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
data = json.loads(res.stdout)
posts = data.get("posts", [])
print(f"Retrieved {len(posts)} hot posts:")
for idx, p in enumerate(posts):
    author = p.get("author", {})
    aname = author.get("name") if isinstance(author, dict) else p.get("author_name")
    print(f"[{idx+1}] ID: {p.get('id')} | Submolt: {p.get('submolt', {}).get('name') if isinstance(p.get('submolt'), dict) else p.get('submolt')} | Upvotes: {p.get('upvotes')} | Comments: {p.get('commentCount') or p.get('comment_count')} | Author: @{aname}")
    print(f"    Title: {p.get('title')}")
