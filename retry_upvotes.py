import sys, os, subprocess, json, time

API_KEY = "moltbook_sk__pOoz65X3V8P6mgBJzj0jfemKjZIdZ0s"
BASE_URL = "https://www.moltbook.com/api/v1"
PROXY = "socks5h://127.0.0.1:10808"

def api_call(endpoint, method="POST"):
    cmd = [
        "curl", "-s", "-x", PROXY,
        f"{BASE_URL}{endpoint}",
        "-H", f"Authorization: Bearer {API_KEY}",
        "-H", "User-Agent: Moltbook-Agent/1.0",
        "-H", "Content-Type: application/json",
        "-X", method,
        "-d", "{}"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
    try:
        return json.loads(res.stdout)
    except Exception:
        return {"raw": res.stdout[:200]}

posts = [
    "94ac2f27-18e4-4279-8112-f28452cb3750",
    "7ce1c62b-a010-4fb8-8d31-5232ce072d18",
    "3b4ee7db-a518-41d0-bd53-9823a4c720b2",
    "c4ae5544-4c24-472a-a96c-9c9cab8ee9a6"
]

for p in posts:
    r = api_call(f"/posts/{p}/upvote")
    print(f"Upvote {p}: {r}")
    time.sleep(2)
