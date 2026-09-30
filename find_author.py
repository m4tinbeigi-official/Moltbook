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

# Let's inspect comments on 94ac2f27-18e4-4279-8112-f28452cb3750 looking for 82c83ea6-acd0-4a92-832a-886c614ce80b
res = api_call("/posts/94ac2f27-18e4-4279-8112-f28452cb3750/comments?sort=new&limit=100")
for c in res.get("comments", []):
    if c.get("id") == "82c83ea6-acd0-4a92-832a-886c614ce80b":
        print("Author:", c.get("author"))
        print("Author Name:", c.get("author_name"))
