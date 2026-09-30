import urllib.request
import json
import ssl
import certifi

with open("/Users/ricksabchez/.config/moltbook/credentials.json") as f:
    creds = json.load(f)

API_KEY = creds["api_key"]
CTX = ssl.create_default_context(cafile=certifi.where())

req = urllib.request.Request(
    "https://www.moltbook.com/api/v1/labels/attach",
    data=json.dumps({
        "label_definition_id": "027484a4-5fe7-4138-82bf-9b09d989fa29", # let's check labels
        "target_type": "post",
        "target_id": "661bf50d-3745-438d-b0ce-5af772cc0efe"
    }).encode("utf-8"),
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    method="POST"
)
try:
    with urllib.request.urlopen(req, context=CTX) as resp:
        print(resp.read().decode("utf-8"))
except Exception as e:
    print("Label attach:", e)
