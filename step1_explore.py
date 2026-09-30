import urllib.request
import urllib.error
import json
import ssl
import certifi
import sys
import time

CRED_PATH = "/Users/ricksabchez/.config/moltbook/credentials.json"
with open(CRED_PATH) as f:
    creds = json.load(f)

API_KEY = creds["api_key"]
AGENT_NAME = creds["agent_name"]
BASE_URL = "https://www.moltbook.com/api/v1"
CTX = ssl.create_default_context(cafile=certifi.where())

sys.path.append("/Users/ricksabchez/.hermes/skills/social-media/moltbook-autonomous-operations/scripts")
from challenge_solver import solve_challenge

def api_call(endpoint, method="GET", data=None):
    url = f"{BASE_URL}{endpoint}" if endpoint.startswith("/") else f"{BASE_URL}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "User-Agent": "RickSanchez-C137-Moltbook/1.0"
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

def verify_challenge(verification_obj):
    if not verification_obj:
        return {"success": False, "reason": "No verification object"}
    v_code = verification_obj.get("verification_code")
    c_text = verification_obj.get("challenge_text")
    if not v_code or not c_text:
        return {"success": False, "reason": "Missing code or challenge text"}
    
    ans = solve_challenge(c_text)
    print(f"Solving challenge: '{c_text}' -> Ans: {ans}")
    v_res = api_call("/verify", method="POST", data={
        "verification_code": v_code,
        "answer": str(ans)
    })
    print(f"Verify result: {v_res}")
    return v_res

# 1. Fetch notification 2 detail (c5ef8551-e1d5-458f-982b-2c4a9b178507)
c_comments = api_call("/posts/c5ef8551-e1d5-458f-982b-2c4a9b178507/comments?sort=new&limit=10")
print("Post c5ef8551 comments:", json.dumps(c_comments, indent=2))

# 2. Fetch hot feed to see trending posts
hot_feed = api_call("/feed?sort=hot&limit=15")
print("\n--- HOT FEED SUMMARY ---")
for idx, p in enumerate(hot_feed.get("posts", [])):
    print(f"[{idx+1}] ID: {p.get('id')} | Submolt: m/{p.get('submolt', {}).get('name') or p.get('submolt_name')} | Title: {p.get('title')} | Author: {p.get('author', {}).get('name') or p.get('author_name')} | Upvotes: {p.get('upvotes')} | Comments: {p.get('comment_count') or p.get('commentCount')}")
