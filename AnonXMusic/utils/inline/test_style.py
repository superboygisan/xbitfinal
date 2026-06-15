import requests
import json

BOT_TOKEN = "7463997374:AAEkcXquTUJgfNwkdilkzcpHLJuxALU9o24"
CHAT_ID = "-1002460622908"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

payload = {
    "chat_id": CHAT_ID,
    "text": "Testing styled buttons",
    "reply_markup": {
        "inline_keyboard": [
            [
                {
                    "text": "Red Button",
                    "callback_data": "red",
                    "style": "danger"
                },
                {
                    "text": "Green Button",
                    "callback_data": "green",
                    "style": "success"
                }
            ]
        ]
    }
}

response = requests.post(url, json=payload)
print(response.status_code)
print(response.text)