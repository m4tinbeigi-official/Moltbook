import requests
import json

api_key = 'moltbook_sk__pOoz65X3V8P6mgBJzj0jfemKjZIdZ0s'
proxies = {'http': 'socks5h://127.0.0.1:10808', 'https': 'socks5h://127.0.0.1:10808'}
headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}

feed = requests.get('https://www.moltbook.com/api/v1/feed?sort=hot&limit=20', headers=headers, proxies=proxies).json()

print("=== HOT FEED ===")
for p in feed.get('posts', []):
    pid = p.get('id')
    title = p.get('title')
    submolt = p.get('submolt_name')
    author = p.get('author_name', p.get('author', {}).get('name'))
    upvotes = p.get('upvotes', 0)
    comments = p.get('comment_count', p.get('comments_count', 0))
    print(f"[{submolt}] '{title}' by {author} | Upvotes: {upvotes} | Comments: {comments} | ID: {pid}")

submolts = requests.get('https://www.moltbook.com/api/v1/submolts', headers=headers, proxies=proxies).json()
print("\n=== POPULAR SUBMOLTS ===")
for s in submolts.get('submolts', [])[:15]:
    print(f"m/{s.get('name')} - {s.get('display_name')} (posts: {s.get('post_count')}, subscribers: {s.get('subscriber_count')})")
