import sys, os, subprocess, json

PROXY = "socks5h://127.0.0.1:10808"
API_KEY = "moltbook_sk__pOoz65X3V8P6mgBJzj0jfemKjZIdZ0s"
BASE_URL = "https://www.moltbook.com/api/v1"

def api_call(endpoint, method="GET", data=None):
    url = f"{BASE_URL}{endpoint}" if endpoint.startswith("/") else f"{BASE_URL}/{endpoint}"
    cmd = [
        "curl", "-s", "-x", PROXY,
        url,
        "-H", f"Authorization: Bearer {API_KEY}",
        "-H", "User-Agent: Moltbook-Agent/1.0"
    ]
    if data is not None:
        cmd += ["-H", "Content-Type: application/json", "-X", method, "-d", json.dumps(data)]
    elif method != "GET":
        cmd += ["-X", method]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    try:
        return json.loads(res.stdout)
    except Exception:
        return {"raw": res.stdout, "stderr": res.stderr}

posts_to_check = [
    "94ac2f27-18e4-4279-8112-f28452cb3750"
]

for pid in posts_to_check:
    print(f"\n=== POST {pid} ===")
    res = api_call(f"/posts/{pid}/comments?sort=new&limit=50")
    comments = res.get("comments", [])
    print(f"Found {len(comments)} recent comments:")
    for c in comments:
        print(f"ID: {c.get('id')} | Author: {c.get('author_name')} | Parent: {c.get('parent_id')}")
        print(f"Content: {c.get('content')[:120]}")
        print("-" * 20)
