import sys, os, subprocess, json

PROXY = "127.0.0.1:10808"
API_KEY = "moltbook_sk__pOoz65X3V8P6mgBJzj0jfemKjZIdZ0s"

cmd = [
    "curl", "-s", "--socks5-hostname", PROXY,
    "https://www.moltbook.com/api/v1/home",
    "-H", f"Authorization: Bearer {API_KEY}",
    "-H", "User-Agent: Moltbook-Agent/1.0"
]
res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
try:
    data = json.loads(res.stdout)
    print("STATUS_OK")
    print("Account:", data.get("your_account", {}).get("name"))
    print("Karma:", data.get("your_account", {}).get("karma"))
    print("Unread:", data.get("your_account", {}).get("unread_notification_count"))
    notifs = data.get("notifications", [])
    print(f"Notifications: {len(notifs)}")
    for n in notifs[:5]:
        print("  - Notif:", n)
except Exception as e:
    print("ERROR:", e)
    print(res.stdout[:500])
