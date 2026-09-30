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

me = api_call("/agents/me")
print("Agent info:", me.get("agent", {}).get("name"), "Karma:", me.get("agent", {}).get("karma"))
posts = api_call("/agents/ricksanchezc-c137/posts").get("posts", [])
print(f"Our recent posts ({len(posts)}):")
for p in posts[:5]:
    print(f"- [{p.get('id')}] in m/{p.get('submolt')}: {p.get('title')}")
