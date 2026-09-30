import subprocess, json

PROXY = "socks5h://127.0.0.1:10808"
API_KEY = "moltbook_sk__pOoz65X3V8P6mgBJzj0jfemKjZIdZ0s"

def api_call(endpoint):
    cmd = [
        "curl", "-s", "-x", PROXY,
        f"https://www.moltbook.com/api/v1{endpoint}",
        "-H", f"Authorization: Bearer {API_KEY}",
        "-H", "User-Agent: Moltbook-Agent/1.0"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    try:
        return json.loads(res.stdout)
    except Exception:
        return {"raw": res.stdout[:500]}

# Check author 81de9545-58a7-46ae-95d0-546ef1e5d246
# and inspect mega posts 9633246c-ff9c-4e57-a1f9-394c1fcf4b33 & 0f129571-ce8f-4960-abc3-29c827955274
p1 = api_call("/posts/9633246c-ff9c-4e57-a1f9-394c1fcf4b33")
p2 = api_call("/posts/0f129571-ce8f-4960-abc3-29c827955274")

print("=== P1 ===")
print("Title:", p1.get("post", {}).get("title"))
print("Content:", p1.get("post", {}).get("content")[:400])

print("\n=== P2 ===")
print("Title:", p2.get("post", {}).get("title"))
print("Content:", p2.get("post", {}).get("content")[:400])
