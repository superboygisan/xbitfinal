from typing import Union

from pyrogram.types import InlineKeyboardMarkup

from AnonXMusic import app


def help_pannel(_, is_sudo, START: Union[bool, int] = None):

    first = [
        {
            "text": f"🌛 {_['CLOSE_BUTTON']}",
            "callback_data": "close",
            "style": "danger"
        }
    ]

    second = [
        {
            "text": f"🌛 {_['BACK_BUTTON']}",
            "callback_data": "settingsback_helper",
            "style": "primary"
        }
    ]

    mark = second if START else first

    upl = [
        [
            {
                "text": f"🌛 {_['H_B_1']}",
                "callback_data": "help_callback hb1",
                "style": "primary"
            },
            {
                "text": f"🌛 {_['H_B_2']}",
                "callback_data": "help_callback hb2",
                "style": "primary"
            },
            {
                "text": f"🌛 {_['H_B_3']}",
                "callback_data": "help_callback hb3",
                "style": "primary"
            },
        ],
        [
            {
                "text": f"🌛 {_['H_B_4']}",
                "callback_data": "help_callback hb4",
                "style": "primary"
            },
            {
                "text": f"🌛 {_['H_B_5']}",
                "callback_data": "help_callback hb5",
                "style": "primary"
            },
            {
                "text": f"🌛 {_['H_B_6']}",
                "callback_data": "help_callback hb6",
                "style": "primary"
            },
        ],
        [
            {
                "text": f"🌛 {_['H_B_7']}",
                "callback_data": "help_callback hb7",
                "style": "primary"
            },
            {
                "text": f"🌛 {_['H_B_8']}",
                "callback_data": "help_callback hb8",
                "style": "primary"
            },
            {
                "text": f"🌛 {_['H_B_9']}",
                "callback_data": "help_callback hb9",
                "style": "primary"
            },
        ],
        [
            {
                "text": f"🌛 {_['H_B_10']}",
                "callback_data": "help_callback hb10",
                "style": "primary"
            },
            {
                "text": f"🌛 {_['H_B_11']}",
                "callback_data": "help_callback hb11",
                "style": "primary"
            },
            {
                "text": f"🌛 {_['H_B_12']}",
                "callback_data": "help_callback hb12",
                "style": "primary"
            },
        ],
        [
            {
                "text": f"🌛 {_['H_B_13']}",
                "callback_data": "help_callback hb13",
                "style": "primary"
            },
            {
                "text": f"🌛 {_['H_B_14']}",
                "callback_data": "help_callback hb14",
                "style": "primary"
            },
            {
                "text": f"🌛 {_['H_B_15']}",
                "callback_data": "help_callback hb15",
                "style": "primary"
            },
        ]
    ]

    if is_sudo:
        upl.append(
            [
                {
                    "text": "🌛 Ai/TTS/IMAGE",
                    "callback_data": "help_callback hb16",
                    "style": "success"
                }
            ]
        )

    upl.append(mark)

    return {"inline_keyboard": upl}


def help_back_markup(_):

    upl = {
        "inline_keyboard": [
            [
                {
                    "text": f"🌛 {_['BACK_BUTTON']}",
                    "callback_data": "settings_back_helper",
                    "style": "primary"
                }
            ]
        ]
    }

    return upl


def private_help_panel(_):

    buttons = {
        "inline_keyboard": [
            [
                {
                    "text": f"🌛 {_['S_B_4']}",
                    "url": f"https://t.me/{app.username}?start=help",
                    "style": "success"
                }
            ]
        ]
    }

    return buttons