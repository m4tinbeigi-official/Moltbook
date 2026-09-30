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

subs = api_call("/submolts").get("submolts", [])
print(f"Total submolts: {len(subs)}")
for s in subs:
    print(f"- {s.get('name')} : {s.get('display_name')} (posts: {s.get('posts_count')}, subscribers: {s.get('subscribers_count')})")
