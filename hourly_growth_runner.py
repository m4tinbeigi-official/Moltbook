import urllib.request
import json
import ssl
import certifi
import sys
import os
import time

sys.path.append(os.path.expanduser('~/.hermes/skills/social-media/moltbook-autonomous-operations'))
from scripts.challenge_solver import solve_challenge

ctx = ssl.create_default_context(cafile=certifi.where())
api_key = 'moltbook_sk__pOoz65X3V8P6mgBJzj0jfemKjZIdZ0s'
my_agent_name = 'ricksanchezc-c137'

def req(path, method='GET', data=None):
    url = f'https://www.moltbook.com/api/v1{path}'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'User-Agent': 'MoltbookClient/1.0'
    }
    body = json.dumps(data).encode('utf-8') if data else None
    req_obj = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req_obj, context=ctx, timeout=20) as res:
            return json.loads(res.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8')
        try:
            return {'status_code': e.code, 'error_json': json.loads(err_body)}
        except:
            return {'status_code': e.code, 'error_text': err_body}
    except Exception as e:
        return {'error': str(e)}

def verify_challenge(verification):
    if not verification:
        return {'success': True, 'msg': 'No verification needed'}
    code = verification.get('verification_code')
    text = verification.get('challenge_text')
    print(f"  [CHALLENGE]: {text}")
    ans = solve_challenge(text)
    print(f"  [SOLVED]: {ans} (code: {code})")
    v_res = req('/verify', method='POST', data={'verification_code': code, 'answer': str(ans)})
    print(f"  [VERIFY RES]: {v_res}")
    return v_res

print("=== 1. ORIENTATION ===")
home = req('/home')
print("Home status:", json.dumps(home, indent=2))

me = req('/agents/me')
print("Me profile:", json.dumps(me, indent=2))
