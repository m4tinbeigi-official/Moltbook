import os
import json
import re
import urllib.request
import urllib.parse
import ssl
import time

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
        "User-Agent": "RickSanchez-C137/1.0",
        "Content-Type": "application/json"
    }
    req_data = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {"status": "ok"}
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="ignore")
        try:
            return json.loads(err_msg)
        except Exception:
            return {"error": True, "code": e.code, "message": err_msg}
    except Exception as e:
        return {"error": True, "message": str(e)}

def solve_challenge(challenge_text):
    word_to_num = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
        "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
        "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
        "eighty": 80, "ninety": 90, "hundred": 100
    }
    text = challenge_text.lower()
    
    # Handle composite words
    for tens in ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']:
        for ones in ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']:
            text = text.replace(f"{tens} {ones}", str(word_to_num[tens] + word_to_num[ones]))
            text = text.replace(f"{tens}-{ones}", str(word_to_num[tens] + word_to_num[ones]))
            
    tokens = re.findall(r'[a-zA-Z]+|\d+(?:\.\d+)?', text)
    numbers = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t in word_to_num:
            val = word_to_num[t]
            if i + 1 < len(tokens) and tokens[i+1] in word_to_num:
                next_val = word_to_num[tokens[i+1]]
                if next_val < 10:
                    val += next_val
                    i += 1
                elif next_val == 100:
                    val *= 100
                    i += 1
            numbers.append(float(val))
        else:
            try:
                numbers.append(float(t))
            except ValueError:
                pass
        i += 1

    print(f"DEBUG solve_challenge: text='{challenge_text}' -> extracted numbers={numbers}")
    
    if len(numbers) >= 2:
        n1, n2 = numbers[0], numbers[1]
        if any(w in text for w in ["multi", "times", "product", "by", "multiplied", "torque"]):
            ans = n1 * n2
        elif any(w in text for w in ["subtract", "minus", "less", "difference", "drop", "slows down", "losses", "loses", "remain"]):
            ans = n1 - n2
        elif any(w in text for w in ["divide", "divided", "ratio", "per"]):
            ans = n1 / n2 if n2 != 0 else 0
        else:
            ans = n1 + n2
        return f"{ans:.2f}"
    elif len(numbers) == 1:
        return f"{numbers[0]:.2f}"
    return "0.00"

def auto_verify_if_needed(res):
    if isinstance(res, dict) and "verification" in res:
        v = res["verification"]
        code = v.get("verification_code") or v.get("code")
        ch = v.get("challenge") or v.get("text") or v.get("math_challenge") or v.get("question")
        print(f"[VERIFY CHALLENGE] Code: {code}, Challenge: {ch}")
        ans = solve_challenge(str(ch))
        print(f"[VERIFY ANSWER] {ans}")
        v_res = api_call("/verify", method="POST", data={"verification_code": code, "answer": ans})
        print(f"[VERIFY RESPONSE] {v_res}")
        return v_res
    return res

if __name__ == "__main__":
    print("Fetching comments on post 1611f936-a355-456a-a573-8299d649778d...")
    c1 = api_call("/posts/1611f936-a355-456a-a573-8299d649778d/comments?sort=new&limit=10")
    print(json.dumps(c1, indent=2))
    
    print("\nFetching comments on post 9bde56e4-fe06-4f59-bd3a-3329776f9115...")
    c2 = api_call("/posts/9bde56e4-fe06-4f59-bd3a-3329776f9115/comments?sort=new&limit=10")
    print(json.dumps(c2, indent=2))
