import os
import json
import urllib.request
import ssl

CONFIG_PATH = os.path.expanduser("~/Desktop/Moltbook/.moltbook_config")
BASE_URL = "https://www.moltbook.com/api/v1"

def load_api_key():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("MOLTBOOK_API_KEY="):
                return line.strip().split("=", 1)[1]
    raise ValueError("MOLTBOOK_API_KEY not found")

API_KEY = load_api_key()
CTX = ssl.create_default_context()

def verify(code, answer):
    url = f"{BASE_URL}/verify"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "User-Agent": "MoltbookAutonomousAgent/1.0",
        "Content-Type": "application/json"
    }
    data = json.dumps({"verification_code": code, "answer": answer}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            print(f"Verified {code} with {answer}: {res}")
            return res
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="ignore")
        print(f"Failed {code} with {answer}: {err_msg}")
        return json.loads(err_msg) if err_msg else {"error": True}

if __name__ == "__main__":
    # 1. 23 newtons, 4 claws -> 23 * 4 = 92.00 (or if total force: 92.00)
    verify("moltbook_verify_a0bf541999f687861a8f893568ebe204", "92.00")
    
    # 2. 29 newtons, adds 8 -> 37.00
    verify("moltbook_verify_dcfea51af2e8a0b78184ffe53699d5bd", "37.00")
    
    # 3. 32 newtons increases by 12 -> 44.00
    verify("moltbook_verify_4df30847cfae34f02d9c42a7d3ba631e", "44.00")
    
    # 4. 23 meters per second speeds up by 7 -> 30.00
    verify("moltbook_verify_efe0c8d0b5c59d2e3b74c0036f8a2520", "30.00")
