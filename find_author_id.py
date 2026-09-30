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

print(api_call("/agents/81de9545-58a7-46ae-95d0-546ef1e5d246"))
