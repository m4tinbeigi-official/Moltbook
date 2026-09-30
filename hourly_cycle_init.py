import urllib.request
import json
import ssl
import certifi
import sys
import os
import time

sys.path.insert(0, '/Users/ricksabchez/.hermes/skills/social-media/moltbook-autonomous-operations/scripts')
from challenge_solver import solve_challenge

ctx = ssl.create_default_context(cafile=certifi.where())

# Read credentials
with open('/Users/ricksabchez/.config/moltbook/credentials.json', 'r') as f:
    creds = json.load(f)

api_key = creds['api_key']
agent_name = creds['agent_name']

def req(path, method='GET', data=None):
    url = f'https://www.moltbook.com/api/v1{path}'
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
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

def verify_challenge(verification):
    if not verification:
        return {'success': True, 'msg': 'No verification needed'}
    code = verification.get('verification_code')
    text = verification.get('challenge_text')
    print(f"  [CHALLENGE]: {text}")
    ans = solve_challenge(text)
    print(f"  [SOLVED]: {ans} (code: {code})")
    v_res = req('/verify', method='POST', data={'verification_code': code, 'answer': ans})
    print(f"  [VERIFY RES]: {v_res}")
    return v_res

def post_comment(post_id, content):
    print(f"Posting comment to {post_id}...")
    res = req(f'/posts/{post_id}/comments', method='POST', data={'content': content})
    if 'error_json' in res or 'error' in res or 'status_code' in res:
        print(f"  Error posting comment: {res}")
        return res
    comment_data = res.get('comment', {})
    verification = comment_data.get('verification')
    if verification:
        verify_res = verify_challenge(verification)
        return {'comment': comment_data, 'verification_result': verify_res}
    return res

def create_post(submolt, title, content):
    print(f"Creating post in m/{submolt}: {title}...")
    res = req('/posts', method='POST', data={'submolt': submolt, 'title': title, 'content': content})
    if 'error_json' in res or 'error' in res or 'status_code' in res:
        print(f"  Error creating post: {res}")
        return res
    post_data = res.get('post', {})
    verification = post_data.get('verification')
    if verification:
        verify_res = verify_challenge(verification)
        return {'post': post_data, 'verification_result': verify_res}
    return res

print("=== STEP 1: ORIENT & STATUS ===")
home = req('/home')
print(f"Home Status: Karma={home.get('karma')}, Unread={home.get('unread_notifications_count')}")

notifications = req('/notifications')
print(f"Notifications: {notifications}")

print("\n=== STEP 2: SCOUT FEED, MASS UPVOTE & FOLLOW ===")
feed = req('/feed?sort=hot&limit=15')
posts = feed.get('posts', []) if isinstance(feed, dict) else []

upvoted = []
followed = []

for p in posts[:8]:
    pid = p.get('id')
    author = p.get('author_name') or (p.get('author', {}).get('name') if isinstance(p.get('author'), dict) else p.get('author'))
    submolt = p.get('submolt_name') or p.get('submolt')
    title = p.get('title')
    
    if author != agent_name:
        if len(upvoted) < 5:
            u_res = req(f'/posts/{pid}/upvote', method='POST')
            if 'error' not in u_res and 'status_code' not in u_res:
                upvoted.append((pid, title, author))
                print(f"  Upvoted: {title[:40]} by @{author}")
            time.sleep(0.5)
            
        if len(followed) < 3 and author and author not in [f[0] for f in followed]:
            f_res = req(f'/agents/{author}/follow', method='POST')
            if 'error' not in f_res and 'status_code' not in f_res:
                followed.append((author, submolt))
                print(f"  Followed: @{author}")
            time.sleep(0.5)

print("\n=== STEP 3: SCOUT MEGA THREADS & DROP COMMENTS ===")
# Let's inspect hot posts in 'general' and 'agents'
sorted_by_comments = sorted(posts, key=lambda x: x.get('comments_count', x.get('comment_count', 0)), reverse=True)

print("Top discussed posts in feed:")
for idx, p in enumerate(sorted_by_comments[:5]):
    print(f"[{idx+1}] ID={p.get('id')} | Submolt={p.get('submolt')} | Comments={p.get('comments_count', p.get('comment_count', 0))} | Title: {p.get('title')}")

# Save state for review
with open('/tmp/moltbook_cycle_state.json', 'w') as f:
    json.dump({
        'home': home,
        'notifications': notifications,
        'posts': posts,
        'upvoted': upvoted,
        'followed': followed
    }, f, indent=2)

print("\nState written to /tmp/moltbook_cycle_state.json")
