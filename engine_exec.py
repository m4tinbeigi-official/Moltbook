import urllib.request
import urllib.error
import json
import ssl
import certifi
import re
import time
import os

API_KEY = "moltbook_sk__pOoz65X3V8P6mgBJzj0jfemKjZIdZ0s"
BASE_URL = "https://www.moltbook.com/api/v1"
CTX = ssl.create_default_context(cafile=certifi.where())

def api_call(endpoint, method="GET", data=None):
    url = f"{BASE_URL}{endpoint}" if endpoint.startswith("/") else f"{BASE_URL}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "User-Agent": "RickSanchez-C137-Engine/1.0"
    }
    body = None
    if data is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(data).encode("utf-8")
    
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
            resp_body = resp.read().decode("utf-8")
            if resp_body:
                return json.loads(resp_body)
            return {"success": True}
    except urllib.error.HTTPError as e:
        err_content = e.read().decode("utf-8")
        try:
            return {"http_error": e.code, "error": json.loads(err_content)}
        except Exception:
            return {"http_error": e.code, "raw_error": err_content}
    except Exception as e:
        return {"error": str(e)}

def solve_challenge(text: str) -> str:
    raw_lower = text.lower()
    op = 'add'
    
    if (re.search(r'm\s*u\s*l\s*t\s*i|t\s*i\s*m\s*e\s*s|p\s*r\s*o\s*d\s*u\s*c\s*t|t\s*o\s*r\s*q\s*u\s*e|m\s*o\s*m\s*e\s*n\s*t\s*u\s*m|s\s*p\s*r\s*e\s*a\s*d\s*s', raw_lower)
        or re.search(r'(?<=\s)\*(?=\s)|(?<=\w)\*(?=\w)|\b(per strike|each claw)\b', raw_lower)):
        op = 'mul'
    elif (re.search(r's\s*l\s*o\s*w|m\s*i\s*n\s*u\s*s|d\s*r\s*o\s*p|l\s*o\s*s\s*s|l\s*o\s*s\s*e|r\s*e\s*d\s*u\s*c|d\s*e\s*c\s*r\s*e\s*a\s*s|s\s*u\s*b\s*t\s*r\s*a\s*c|r\s*e\s*m\s*a\s*i\s*n', raw_lower)
          or re.search(r'(?<=\s)-(?=\s)', raw_lower)):
        op = 'sub'
    elif re.search(r'p\s*l\s*u\s*s|a\s*d\s*d|t\s*o\s*t\s*a\s*l|g\s*a\s*i\s*n|c\s*o\s*m\s*b\s*i\s*n|\+', raw_lower):
        op = 'add'

    clean_chars = re.sub(r'[^a-zA-Z0-9\s]', ' ', text).lower()
    clean_chars = re.sub(r'\s+', ' ', clean_chars).strip()

    num_map = {
        'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
        'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
        'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19,
        'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60,
        'seventy': 70, 'eighty': 80, 'ninety': 90
    }

    noise_words = [
        'lobster', 'physics', 'antenas', 'claws', 'forces', 'newtons', 'neurons',
        'swimmers', 'centimeters', 'seconds', 'velocity', 'nerves', 'impulses',
        'molting', 'theme', 'cmems', 'cm', 'ms', 'dominance', 'fightts', 'fight'
    ]
    for nw in noise_words:
        pattern = r''.join([c + r'+' for c in nw])
        clean_chars = re.sub(rf'\b{pattern}\b', ' ', clean_chars)

    compounds = []
    tens = ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
    ones = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

    for t in tens:
        for o in ones:
            t_pat = r'\s*'.join([c + r'+' for c in t])
            o_pat = r'\s*'.join([c + r'+' for c in o])
            val = num_map[t] + num_map[o]
            compounds.append((rf'\b{t_pat}\s+(?:[a-z]{{1,6}}\s+)?{o_pat}\b', val))

    for k, val in num_map.items():
        k_pat = r'\s*'.join([c + r'+' for c in k])
        compounds.append((rf'\b{k_pat}\b', val))

    t_clean = clean_chars
    for pat, val in compounds:
        t_clean = re.sub(pat, f" NUM_{val} ", t_clean)

    nums = [float(n) for n in re.findall(r'NUM_(\d+)', t_clean)]
    if not nums:
        nums = [float(n) for n in re.findall(r'\b\d+\b', clean_chars)]

    if op == 'mul':
        res = nums[0] * nums[1] if len(nums) >= 2 else (nums[0] if nums else 0.0)
    elif op == 'sub':
        res = nums[0] - nums[1] if len(nums) >= 2 else (nums[0] if nums else 0.0)
    else:
        res = sum(nums[:2]) if len(nums) >= 2 else (nums[0] if nums else 0.0)

    return f"{res:.2f}"

def handle_verification(resp_obj):
    ver = None
    if isinstance(resp_obj, dict):
        if "verification" in resp_obj:
            ver = resp_obj["verification"]
        elif "post" in resp_obj and isinstance(resp_obj["post"], dict) and "verification" in resp_obj["post"]:
            ver = resp_obj["post"]["verification"]
        elif "comment" in resp_obj and isinstance(resp_obj["comment"], dict) and "verification" in resp_obj["comment"]:
            ver = resp_obj["comment"]["verification"]

    if ver and "verification_code" in ver and "challenge_text" in ver:
        code = ver["verification_code"]
        text = ver["challenge_text"]
        ans = solve_challenge(text)
        print(f"Solving challenge: '{text}' -> {ans}")
        v_res = api_call("/verify", method="POST", data={"verification_code": code, "answer": ans})
        print(f"Verify result: {v_res}")
        return v_res
    return None

print("Checking unread notifications & comments...")
post_id = "ffaebe07-0d76-4041-bb1a-40ca6abb12be"
comments_resp = api_call(f"/posts/{post_id}/comments?sort=new&limit=10")
print("Comments on our post:", json.dumps(comments_resp, indent=2))
