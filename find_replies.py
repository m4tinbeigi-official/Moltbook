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
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    try:
        return json.loads(res.stdout)
    except Exception:
        return {"raw": res.stdout[:500]}

notifs_res = api_call("/notifications")
unread = [n for n in notifs_res.get("notifications", []) if not n.get("isRead")]
print(f"Unread count: {len(unread)}")
for n in unread:
    print(json.dumps(n, indent=2))
    cid = n.get("relatedCommentId")
    pid = n.get("relatedPostId")
    if pid and cid:
        c_res = api_call(f"/posts/{pid}/comments?sort=new&limit=100")
        for c in c_res.get("comments", []):
            if c.get("id") == cid or c.get("parent_id") == cid:
                print("FOUND COMMENT:", json.dumps(c, indent=2))
