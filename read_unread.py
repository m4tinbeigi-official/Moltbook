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

# 1. Comment on e555c9cc (5cd8f232)
c1 = api_call("/posts/e555c9cc-e496-48a8-b0f2-4793da7fa5a1/comments?limit=20")
for c in c1.get("comments", []):
    if c.get("id") == "5cd8f232-8fae-4f78-8fe1-c7a3ad4c4b61":
        print("=== Comment on e555c9cc ===")
        print("Author:", c.get("author_name") or c.get("author"))
        print("Content:", c.get("content"))

# 2. Comments on 1482e8df
c2 = api_call("/posts/1482e8df-7064-4443-a1ee-6e62e43e70e3/comments?limit=20")
for c in c2.get("comments", []):
    if c.get("id") in ["6ee3776a-fd71-46d5-be06-ba93894475e9", "602349b9-07b8-42a4-b42c-97792bf50921"]:
        print(f"=== Comment on 1482e8df by @{c.get('author_name') or c.get('author')} ===")
        print("Content:", c.get("content"))
