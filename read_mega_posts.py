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

p1 = api_call("/posts/9633246c-ff9c-4e57-a1f9-394c1fcf4b33")
print("=== P1 ===")
print("Title:", p1.get("post", {}).get("title"))
print("Content:", p1.get("post", {}).get("content")[:400])

p2 = api_call("/posts/b075188e-e30c-460b-bdd1-341c03bbaf37")
print("\n=== P2 ===")
print("Title:", p2.get("post", {}).get("title"))
print("Content:", p2.get("post", {}).get("content")[:400])
