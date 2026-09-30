#!/usr/bin/env python3
import os
import sys
import json
import re
import urllib.request
import urllib.parse
import ssl

CONFIG_PATH = os.path.expanduser("~/Desktop/Moltbook/.moltbook_config")
BASE_URL = "https://www.moltbook.com/api/v1"

def load_api_key():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Config not found at {CONFIG_PATH}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("MOLTBOOK_API_KEY="):
                return line.strip().split("=", 1)[1]
    raise ValueError("MOLTBOOK_API_KEY not found in config")

API_KEY = load_api_key()
CTX = ssl.create_default_context()

def api_request(endpoint, method="GET", data=None):
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
        return {"error": True, "code": e.code, "message": err_msg}
    except Exception as e:
        return {"error": True, "message": str(e)}

def parse_challenge_and_solve(challenge_text):
    # Normalize challenge text
    cleaned = re.sub(r'[^a-zA-Z0-9\s\.\,\+\-\*\/\^]', '', challenge_text)
    
    # Word to number mapping
    words_to_num = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
        "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
        "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
        "eighty": 80, "ninety": 90, "hundred": 100
    }
    
    # Extract numbers or words
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

    # Heuristic math based on common challenge operators
    text_lower = challenge_text.lower()
    if len(numbers) >= 2:
        n1, n2 = numbers[0], numbers[1]
        if "multi" in text_lower or "times" in text_lower or "product" in text_lower or "by" in text_lower:
            ans = n1 * n2
        elif "add" in text_lower or "plus" in text_lower or "total" in text_lower or "sum" in text_lower:
            ans = n1 + n2
        elif "subtract" in text_lower or "minus" in text_lower or "less" in text_lower:
            ans = n1 - n2
        elif "divide" in text_lower or "divided" in text_lower:
            ans = n1 / n2 if n2 != 0 else 0
        else:
            ans = n1 + n2
        return f"{ans:.2f}"
    return None

def verify_submission(code, challenge_text):
    ans = parse_challenge_and_solve(challenge_text)
    if ans:
        res = api_request("/verify", method="POST", data={"verification_code": code, "answer": ans})
        return res
    return {"error": True, "message": "Could not solve challenge"}

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "status"
    if action == "status":
        print(json.dumps(api_request("/home"), indent=2))
    elif action == "feed":
        print(json.dumps(api_request("/feed?limit=5"), indent=2))
