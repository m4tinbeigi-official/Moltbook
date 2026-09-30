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
print(f"Total notifications: {len(notifs)}")
for n in notifs:
    print(f"ID: {n.get('id')}, type: {n.get('type')}, post: {n.get('relatedPostId')}, comment: {n.get('relatedCommentId')}, isRead: {n.get('isRead')}")
    # fetch the comment if commentId exists
    cid = n.get('relatedCommentId')
    pid = n.get('relatedPostId')
    if pid:
        post_data = api_call(f"/posts/{pid}")
        post_title = post_data.get("post", {}).get("title")
        print(f"  Post Title: {post_title}")
        # fetch comments of post
        comments_data = api_call(f"/posts/{pid}/comments?sort=new&limit=10")
        comms = comments_data.get("comments", [])
        for c in comms:
            if c.get("id") == cid or not cid:
                c_author = c.get("author_name") or (c.get("author", {}).get("name") if isinstance(c.get("author"), dict) else c.get("author"))
                print(f"  -> Comment by @{c_author}: {c.get('content')[:200]}")
