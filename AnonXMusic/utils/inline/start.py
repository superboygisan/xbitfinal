from AnonXMusic import app
import config


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

    return buttons


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
                    "user_id": config.OWNER_ID,
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
                    "url": "CURRENCY",
                    "style": "danger"
                }
            ],

        ]
    }

    return buttons