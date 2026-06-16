
from pyrogram import enums
from pyrogram.types import InlineKeyboardButton

from config import OWNER_ID, SUPPORT_CHAT, SUPPORT_CHANNEL


def btn(text, style="primary", **kwargs):

    styles = {
        "primary": enums.ButtonStyle.PRIMARY,
        "success": enums.ButtonStyle.SUCCESS,
        "danger": enums.ButtonStyle.DANGER,
        "default": enums.ButtonStyle.DEFAULT,
    }

    return InlineKeyboardButton(
        text=text,
        style=styles.get(style, enums.ButtonStyle.DEFAULT),
        **kwargs
    )


def start_panel(bot_username):
    return [
        [
            btn(
                text="➕ Add Me",
                style="success",
                url=f"https://t.me/{bot_username}?startgroup=true",
            ),
            btn(
                text="💬 Support",
                style="primary",
                url=SUPPORT_CHAT,
            ),
        ],
    ]


def private_panel(bot_username):
    return [
        [
            btn(
                text="➕ Add Me To Group",
                style="success",
                url=f"https://t.me/{bot_username}?startgroup=true",
            )
        ],
        [
            btn(
                text="⚙️ Settings",
                style="primary",
                callback_data="settings_back_helper",
            )
        ],
        [
            btn(
                text="👑 Owner",
                style="danger",
                user_id=OWNER_ID,
            ),
            btn(
                text="📢 Channel",
                style="primary",
                url=SUPPORT_CHANNEL,
            ),
        ],
        [
            btn(
                text="💬 Support Chat",
                style="primary",
                url=SUPPORT_CHAT,
            ),
        ],
    ]
