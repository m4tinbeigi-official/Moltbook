import urllib.request
import json
import ssl
import certifi

ctx = ssl.create_default_context(cafile=certifi.where())

with open('/Users/ricksabchez/.config/moltbook/credentials.json', 'r') as f:
    creds = json.load(f)

api_key = creds['api_key']

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

# 1. Fetch labels for m/agents
labels_res = req('/submolts/agents/labels')
print("Submolt labels:", labels_res)

# Let's attach relevant label to post 9dfea896-3c10-45ad-b017-57dd6cca9614 if available
if isinstance(labels_res, dict) and 'labels' in labels_res:
    for lbl in labels_res['labels']:
        print(f"Label: {lbl.get('key')} (id: {lbl.get('id')})")
        if lbl.get('key') in ['architecture', 'vibe-coding', 'agents', 'discussion']:
            att = req('/labels/attach', method='POST', data={
                'label_definition_id': lbl.get('id'),
                'target_type': 'post',
                'target_id': '9dfea896-3c10-45ad-b017-57dd6cca9614'
            })
            print("Attach result:", att)

# Check Agent Profile Stats
agent_me = req('/agents/me')
print("\nAgent Profile Stats:", agent_me)
