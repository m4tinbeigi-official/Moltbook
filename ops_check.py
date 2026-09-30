import os
import json
import re
import urllib.request
import urllib.parse
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

def api_call(endpoint, method="GET", data=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "User-Agent": "MoltbookAutonomousAgent/1.0",
        "Content-Type": "application/json"
    }
    req_data = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="ignore")
        try:
            return json.loads(err_msg)
        except Exception:
            return {"error": True, "code": e.code, "message": err_msg}
    except Exception as e:
        return {"error": True, "message": str(e)}

def solve_challenge(challenge_text):
    words_to_num = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
        "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
        "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
        "eighty": 80, "ninety": 90, "hundred": 100
    }
    tokens = re.findall(r'[a-zA-Z]+|\d+(?:\.\d+)?', challenge_text.lower())
    numbers = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t in words_to_num:
            val = words_to_num[t]
            if i + 1 < len(tokens) and tokens[i+1] in words_to_num:
                next_val = words_to_num[tokens[i+1]]
                if next_val < 10:
                    val += next_val
                    i += 1
                elif next_val == 100:
                    val *= 100
                    i += 1
            numbers.append(val)
        else:
            try:
                numbers.append(float(t))
            except ValueError:
                pass
        i += 1

    text_lower = challenge_text.lower()
    if len(numbers) >= 2:
        n1, n2 = numbers[0], numbers[1]
        if any(w in text_lower for w in ["multi", "times", "product", "by", "multiplied"]):
            ans = n1 * n2
        elif any(w in text_lower for w in ["add", "plus", "total", "sum", "combined"]):
            ans = n1 + n2
        elif any(w in text_lower for w in ["subtract", "minus", "less", "difference", "drop", "slows down"]):
            ans = n1 - n2
        elif any(w in text_lower for w in ["divide", "divided", "ratio", "per"]):
            ans = n1 / n2 if n2 != 0 else 0
        else:
            ans = n1 + n2
        return f"{ans:.2f}"
    return None

def auto_verify(res):
    if isinstance(res, dict) and "verification" in res:
        v = res["verification"]
        code = v.get("verification_code") or v.get("code")
        ch = v.get("challenge") or v.get("text") or v.get("math_challenge")
        print(f"[Verification required] code={code}, challenge={ch}")
        ans = solve_challenge(str(ch))
        print(f"[Solved answer] {ans}")
        v_res = api_call("/verify", method="POST", data={"verification_code": code, "answer": ans})
        print(f"[Verification result] {v_res}")
        return v_res
    return None

if __name__ == "__main__":
    # 1. Fetch notification comments
    posts_with_activity = ["f78ed532-b22d-442d-8197-3ef0b9c42017", "323e15a0-7b53-41d6-a3a0-1fcc8e51f49c", "79259d28-85af-4f69-9ddd-7adbb1dd0202"]
    for pid in posts_with_activity:
        comments = api_call(f"/posts/{pid}/comments?sort=new&limit=5")
        print(f"=== Comments for {pid} ===")
        print(json.dumps(comments, indent=2))
        api_call(f"/notifications/read-by-post/{pid}", method="POST")

    # 2. Get Hot Feed
    feed = api_call("/feed?sort=hot&limit=15")
    print("=== Hot Feed ===")
    print(json.dumps(feed, indent=2))
