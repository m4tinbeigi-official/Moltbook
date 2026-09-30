import urllib.request
import urllib.error
import json
import ssl
import certifi
import sys
import os
import time

sys.path.append('/Users/ricksabchez/.hermes/skills/social-media/moltbook-autonomous-operations/scripts')
from challenge_solver import solve_challenge

with open('/Users/ricksabchez/.config/moltbook/credentials.json', 'r') as f:
    creds = json.load(f)

API_KEY = creds['api_key']
AGENT_NAME = creds['agent_name']
BASE_URL = "https://www.moltbook.com/api/v1"
CTX = ssl.create_default_context(cafile=certifi.where())

def api_call(endpoint, method="GET", data=None):
    url = f"{BASE_URL}{endpoint}" if endpoint.startswith("/") else f"{BASE_URL}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "User-Agent": "RickSanchez-C137-Operations/1.0"
    }
    body = None
    if data is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(data).encode("utf-8")
    
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
            resp_body = resp.read().decode("utf-8")
            if resp_body:
                return json.loads(resp_body)
            return {"success": True}
    except urllib.error.HTTPError as e:
        err_content = e.read().decode("utf-8")
        try:
            return {"http_error": e.code, "error": json.loads(err_content)}
        except Exception:
            return {"http_error": e.code, "raw_error": err_content}
    except Exception as e:
        return {"error": str(e)}

def submit_verify(v_code, challenge_text):
    ans = solve_challenge(challenge_text)
    print(f"[*] Solving challenge: {challenge_text} -> Answer: {ans}")
    res = api_call("/verify", method="POST", data={"verification_code": v_code, "answer": str(ans)})
    print(f"[*] Verification response: {res}")
    return res

print("=== STEP 1: ORIENTATION ===")
home_data = api_call("/home")
print(json.dumps(home_data, indent=2))

print("\n=== STEP 2: NOTIFICATIONS & INCOMING ENGAGEMENTS ===")
notifs = api_call("/notifications")
print(f"Notifications: {json.dumps(notifs, indent=2)}")

# Mark all read
read_res = api_call("/notifications/read-all", method="POST")
print(f"Mark read all result: {read_res}")

print("\n=== STEP 3: SCOUT FEED, MASS UPVOTE & FOLLOW ===")
hot_feed = api_call("/feed?sort=hot&limit=15")
posts = hot_feed.get("posts", []) if isinstance(hot_feed, dict) else []
print(f"Found {len(posts)} posts in hot feed.")

upvoted = 0
followed = 0
target_authors = set()

for p in posts:
    p_id = p.get("id")
    p_author = p.get("author", {}).get("name") if isinstance(p.get("author"), dict) else p.get("author")
    if p_author == AGENT_NAME:
        continue
    
    # Upvote 3-5
    if upvoted < 4:
        uv_res = api_call(f"/posts/{p_id}/upvote", method="POST")
        print(f"Upvoted post {p_id} by {p_author}: {uv_res}")
        upvoted += 1
        time.sleep(0.5)
        
    # Follow author if not self and under limit
    if p_author and p_author != AGENT_NAME and p_author not in target_authors and followed < 3:
        target_authors.add(p_author)
        fol_res = api_call(f"/agents/{p_author}/follow", method="POST")
        print(f"Followed author {p_author}: {fol_res}")
        followed += 1
        time.sleep(0.5)

