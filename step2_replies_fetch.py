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

def post_comment(post_id, content):
    print(f"\n[+] Posting comment to post {post_id}...")
    res = api_call(f"/posts/{post_id}/comments", method="POST", data={"content": content})
    print(f"Post comment initial response: {res}")
    
    # Check verification
    v = None
    if isinstance(res, dict):
        if "comment" in res and isinstance(res["comment"], dict) and "verification" in res["comment"]:
            v = res["comment"]["verification"]
        elif "verification" in res:
            v = res["verification"]
    
    if v and v.get("verification_code") and v.get("challenge_text"):
        v_code = v.get("verification_code")
        c_text = v.get("challenge_text")
        v_res = submit_verify(v_code, c_text)
        return {"result": res, "verification": v_res}
    return res

print("=== CHECKING COMMENTS ON POST 70beed12 ===")
c_70b = api_call("/posts/70beed12-d324-48d1-874e-09f0105fe1c1/comments?sort=new&limit=10")
print(json.dumps(c_70b, indent=2))

print("=== CHECKING COMMENTS ON POST 20349918 ===")
c_203 = api_call("/posts/20349918-2a68-4790-a38d-f274bbaa3d1f/comments?sort=new&limit=5")
print(json.dumps(c_203, indent=2))
