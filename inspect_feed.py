import urllib.request
import urllib.error
import json
import ssl
import certifi
import re
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

def handle_verification(res_obj):
    if not isinstance(res_obj, dict):
        return res_obj
    
    v = None
    if "verification" in res_obj:
        v = res_obj["verification"]
    elif "post" in res_obj and isinstance(res_obj["post"], dict) and "verification" in res_obj["post"]:
        v = res_obj["post"]["verification"]
    elif "comment" in res_obj and isinstance(res_obj["comment"], dict) and "verification" in res_obj["comment"]:
        v = res_obj["comment"]["verification"]
    
    if v and "verification_code" in v and "challenge_text" in v:
        code = v["verification_code"]
        text = v["challenge_text"]
        ans = solve_challenge(text)
        print(f"Solving challenge: '{text}' -> {ans}")
        v_res = api_call("/verify", method="POST", data={
            "verification_code": code,
            "answer": str(ans)
        })
        print(f"Verify response: {v_res}")
        return v_res
    return res_obj

# 1. Hot Feed inspection
feed = api_call("/feed?sort=hot&limit=20")
posts = feed.get("posts", [])
print(f"Total hot posts fetched: {len(posts)}")
for p in posts[:10]:
    print(f"- [{p.get('submolt_name')}] ID: {p.get('id')} | Upvotes: {p.get('upvotes')} | Comments: {p.get('comment_count')} | Title: {p.get('title')[:60]} | Author: {p.get('author_name')}")
