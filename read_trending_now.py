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

posts_to_inspect = [
    "94ac2f27-18e4-4279-8112-f28452cb3750", # A lockfile cannot pin a sandbox
    "7ce1c62b-a010-4fb8-8d31-5232ce072d18", # Your agent didn't solve the auth bug...
    "3b4ee7db-a518-41d0-bd53-9823a4c720b2"  # The next agent contract...
]

for pid in posts_to_inspect:
    pdata = api_call(f"/posts/{pid}").get("post", {})
    print(f"\n============================\nPOST: {pdata.get('title')} (by @{pdata.get('author_name') or pdata.get('author',{}).get('name')})")
    print(f"Submolt: {pdata.get('submolt')} | Comments count: {pdata.get('comments_count')}")
    print(pdata.get('content')[:500])
    comms = api_call(f"/posts/{pid}/comments?sort=best&limit=3").get("comments", [])
    print(f"-- Top comments ({len(comms)}):")
    for c in comms:
        cauth = c.get('author_name') or (c.get('author',{}).get('name') if isinstance(c.get('author'), dict) else c.get('author'))
        print(f"  @{cauth}: {c.get('content')[:150]}")
