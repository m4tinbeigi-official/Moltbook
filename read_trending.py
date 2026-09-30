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

for pid in ["5c3cddcc-ee9a-41e9-9134-8c01d43171fa", "47cc73c9-f1fb-48ca-8d59-cf212b69ee2f"]:
    p = api_call(f"/posts/{pid}")
    post = p.get("post", {})
    print("="*40)
    print("TITLE:", post.get("title"))
    print("AUTHOR:", post.get("author_name") or post.get("author"))
    print("CONTENT:", post.get("content")[:600])
