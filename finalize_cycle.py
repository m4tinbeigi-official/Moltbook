import subprocess
import json

API_KEY = "moltbook_sk__pOoz65X3V8P6mgBJzj0jfemKjZIdZ0s"
BASE_URL = "https://www.moltbook.com/api/v1"
PROXY = "socks5h://127.0.0.1:10808"

def api_call(endpoint, method="GET", data=None):
    url = f"{BASE_URL}{endpoint}" if endpoint.startswith("/") else f"{BASE_URL}/{endpoint}"
    cmd = [
        "curl", "-s", "-x", PROXY,
        url,
        "-H", f"Authorization: Bearer {API_KEY}",
        "-H", "User-Agent: Moltbook-Agent/1.0"
    ]
    if method != "GET":
        cmd += ["-X", method]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
    try:
        return json.loads(res.stdout)
    except Exception:
        return {"raw": res.stdout}

print("READ ALL:", api_call("/notifications/read-all", method="POST"))
me = api_call("/agents/me")
print("ME:", json.dumps(me.get("agent", {}), indent=2))
