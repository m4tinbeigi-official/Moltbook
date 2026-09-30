import urllib.request
import urllib.error
import json
import ssl
import certifi
import re
import sys
import os

# Load credentials
CRED_PATH = "/Users/ricksabchez/.config/moltbook/credentials.json"
with open(CRED_PATH) as f:
    creds = json.load(f)

API_KEY = creds["api_key"]
AGENT_NAME = creds["agent_name"]
BASE_URL = "https://www.moltbook.com/api/v1"
CTX = ssl.create_default_context(cafile=certifi.where())

# Import challenge solver from skill
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

print("=== STEP 1: ORIENTATION (GET /home) ===")
home = api_call("/home")
print(f"Home response: {json.dumps(home, indent=2)}")

print("\n=== STEP 2: NOTIFICATIONS ===")
notifs = api_call("/notifications")
print(f"Notifications: {json.dumps(notifs, indent=2)}")

print("\n=== STEP 3: SCOUT FEED & FOLLOW ===")
feed = api_call("/feed?sort=hot&limit=15")
posts = feed.get("posts", []) if isinstance(feed, dict) else []
print(f"Fetched {len(posts)} hot posts.")
