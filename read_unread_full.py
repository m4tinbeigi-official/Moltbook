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

notifs_res = api_call("/notifications")
notifs = notifs_res.get("notifications", [])
unread = [n for n in notifs if not n.get("isRead")]
print(f"Found {len(unread)} unread notifications:")

for n in unread:
    nid = n.get("id")
    ntype = n.get("type")
    pid = n.get("relatedPostId")
    cid = n.get("relatedCommentId")
    print(f"\n--- NOTIF {nid} | type: {ntype} | post: {pid} | comment: {cid} ---")
    if pid:
        # get post
        post = api_call(f"/posts/{pid}").get("post", {})
        print(f"Post Title: {post.get('title')}")
        # get comment
        if cid:
            # find comment
            comms = api_call(f"/posts/{pid}/comments?sort=new&limit=25").get("comments", [])
            target_c = next((c for c in comms if c.get("id") == cid), None)
            if target_c:
                c_author = target_c.get("author_name") or (target_c.get("author", {}).get("name") if isinstance(target_c.get("author"), dict) else target_c.get("author"))
                print(f"Comment from @{c_author}: {target_c.get('content')}")
            else:
                print("Comment not found in latest 25")
