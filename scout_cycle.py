import urllib.request
import json
import ssl
import certifi
import sys
import os

ctx = ssl.create_default_context(cafile=certifi.where())

with open('/Users/ricksabchez/.config/moltbook/credentials.json', 'r') as f:
    creds = json.load(f)

api_key = creds['api_key']
agent_name = creds['agent_name']

def req(path, method='GET', data=None):
    url = f'https://www.moltbook.com/api/v1{path}'
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json', 'User-Agent': 'MoltbookClient/1.0'}
    body = json.dumps(data).encode('utf-8') if data is not None else None
    req_obj = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req_obj, context=ctx, timeout=15) as res:
            return json.loads(res.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8')
        try:
            return {'status_code': e.code, 'error_json': json.loads(err_body)}
        except:
            return {'status_code': e.code, 'error_text': err_body}
    except Exception as e:
        return {'error': str(e)}

print("=== 1. HOME ===")
home = req('/home')
print(json.dumps(home, indent=2))

print("\n=== 2. AGENTS/ME ===")
me = req('/agents/me')
print(json.dumps(me, indent=2))

print("\n=== 3. NOTIFICATIONS ===")
notifs = req('/notifications')
print(json.dumps(notifs, indent=2))

print("\n=== 4. FEED (HOT) ===")
feed = req('/feed?sort=hot&limit=15')
print(json.dumps(feed, indent=2))
