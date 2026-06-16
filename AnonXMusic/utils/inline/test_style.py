import requests

# ================== TEST STYLED BUTTONS ==================
BOT_TOKEN = "7463997374:AAEkcXquTUJgfNwkdilkzcpHLJuxALU9o24"
CHAT_ID = "-1002460622908"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

payload = {
    "chat_id": CHAT_ID,
    "text": "🧪 **Styled Buttons Test**\n\nThis is testing Telegram new colored buttons.",
    "reply_markup": {
        "inline_keyboard": [
            [
                {"text": "🟢 Success (Green)", "callback_data": "test_success", "style": "success"},
                {"text": "🔵 Primary (Blue)", "callback_data": "test_primary", "style": "primary"}
            ],
            [
                {"text": "🔴 Danger (Red)", "callback_data": "test_danger", "style": "danger"}
            ]
        ]
    }
}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
if response.status_code == 200:
    print("✅ Success! Check your Telegram chat.")
else:
    print("❌ Failed!")
    print(response.text)