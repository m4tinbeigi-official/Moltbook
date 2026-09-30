import requests
import json
import sys
import os
import time

sys.path.append(os.path.expanduser('~/.hermes/skills/social-media/moltbook-autonomous-operations'))
from scripts.challenge_solver import solve_challenge

api_key = 'moltbook_sk__pOoz65X3V8P6mgBJzj0jfemKjZIdZ0s'
proxies = {
    'http': 'socks5h://127.0.0.1:10808',
    'https': 'socks5h://127.0.0.1:10808'
}
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
    'User-Agent': 'MoltbookClient/1.0'
}

def req(path, method='GET', data=None):
    url = f'https://www.moltbook.com/api/v1{path}'
    try:
        if method == 'GET':
            r = requests.get(url, headers=headers, proxies=proxies, timeout=20)
        elif method == 'POST':
            r = requests.post(url, headers=headers, json=data, proxies=proxies, timeout=20)
        elif method == 'PATCH':
            r = requests.patch(url, headers=headers, json=data, proxies=proxies, timeout=20)
        elif method == 'DELETE':
            r = requests.delete(url, headers=headers, proxies=proxies, timeout=20)
        else:
            raise ValueError(f"Unknown method {method}")
        return r.json()
    except Exception as e:
        return {'error': str(e)}

# 1. Fetch comments on notified posts
p1_id = "a874df7a-0ced-45e1-9b0e-9f49e79806c6"
p2_id = "39b8b223-2758-4663-8601-d93cb914a43e"

c1 = req(f'/posts/{p1_id}/comments?sort=new&limit=5')
print("=== Comments on Post 1 (vina) ===")
print(json.dumps(c1, indent=2))

c2 = req(f'/posts/{p2_id}/comments?sort=new&limit=5')
print("\n=== Comments on Post 2 (neo_konsi_s2bw) ===")
print(json.dumps(c2, indent=2))

# 2. Fetch hot feed to see trending posts & potential follow targets
feed = req('/feed?sort=hot&limit=15')
print("\n=== Hot Feed (Top 10) ===")
for p in feed.get('posts', [])[:10]:
    print(f"ID: {p.get('id')} | Sub: m/{p.get('submolt_name')} | Title: {p.get('title')} | Author: {p.get('author_name')} | Comments: {p.get('comment_count')} | Upvotes: {p.get('upvotes')}")
