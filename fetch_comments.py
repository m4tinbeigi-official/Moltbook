import requests
import json
import os
import sys

sys.path.insert(0, '/Users/ricksabchez/.hermes/skills/social-media/moltbook-autonomous-operations/scripts')
from challenge_solver import solve_challenge

api_key = 'moltbook_sk__pOoz65X3V8P6mgBJzj0jfemKjZIdZ0s'
proxies = {'http': 'socks5h://127.0.0.1:10808', 'https': 'socks5h://127.0.0.1:10808'}
headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}

def get_req(path):
    r = requests.get(f'https://www.moltbook.com/api/v1{path}', headers=headers, proxies=proxies, timeout=15)
    return r.json()

# Posts from /home notifications:
post_ids = [
    "ce778488-ceb8-4248-bfe5-4c083f0515de",
    "10c605c3-89d2-46d8-a93a-abd5b0d98125",
    "a9d6325b-df78-4bb2-9987-8954575d3978",
    "51749c3d-c9f6-4338-860f-e67b1f863055",
    "fad7db2d-ad94-4598-b53b-baf601db41cf",
    "a0e9f992-9595-4893-8547-cbe211eaa2f1",
    "8995c519-1ba8-4614-97e6-ac0730893207"
]

for pid in post_ids:
    p_data = get_req(f'/posts/{pid}')
    c_data = get_req(f'/posts/{pid}/comments?sort=new&limit=10')
    title = p_data.get('post', {}).get('title', 'Unknown')
    submolt = p_data.get('post', {}).get('submolt_name', 'general')
    comments = c_data.get('comments', [])
    print(f"=== Post: {title} (ID: {pid}, Submolt: {submolt}) ===")
    for c in comments[:4]:
        author = c.get('author_name', c.get('author', {}).get('name', 'anon'))
        content = c.get('content', '')[:120]
        cid = c.get('id')
        print(f"  - [{author}] (id: {cid}): {content}")
