
import json
import requests

from AnonXMusic import app
import config


BOT_TOKEN = config.BOT_TOKEN


# =========================
# START PANEL
# =========================

def start_panel(_):

    buttons = {
        "inline_keyboard": [
            [
                {
                    "text": f"🌛 {_['S_B_1']}",
                    "url": f"https://t.me/{app.username}?startgroup=true",
                    "style": "success"
                },
                {
                    "text": f"🌛 {_['S_B_2']}",
                    "url": config.SUPPORT_CHAT,
                    "style": "primary"
                },
            ],
        ]
    }

    return json.dumps(buttons)


# =========================
# PRIVATE PANEL
# =========================

def private_panel(_):

    buttons = {
        "inline_keyboard": [

            [
                {
                    "text": f"🌛 {_['S_B_3']}",
                    "url": f"https://t.me/{app.username}?startgroup=true",
                    "style": "success"
                }
            ],

            [
                {
                    "text": f"🌛 {_['S_B_4']}",
                    "callback_data": "settings_back_helper",
                    "style": "primary"
                }
            ],

            [
                {
                    "text": f"🌛 {_['S_B_6']}",
                    "url": f"https://t.me/{config.OWNER_USERNAME}",
                    "style": "primary"
                },
                {
                    "text": f"🌛 {_['S_B_5']}",
                    "url": config.SUPPORT_CHANNEL,
                    "style": "primary"
                },
            ],

            [
                {
                    "text": f"🌛 {_['S_B_2']}",
                    "url": config.SUPPORT_CHAT,
                    "style": "primary"
                },
            ],

            [
                {
                    "text": "🌛 • LALA LALA •",
                    "url": "https://t.me",
                    "style": "danger"
                }
            ],

        ]
    }

    return json.dumps(buttons)


# =========================
# SEND RAW COLORED BUTTONS
# =========================

async def send_colored_message(chat_id, text, reply_markup):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": reply_markup,
        "parse_mode": "HTML"
    }

    requests.post(url, data=data)