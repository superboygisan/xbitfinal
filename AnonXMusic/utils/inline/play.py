import math

from pyrogram.types import InlineKeyboardButton
from AnonXMusic.utils.formatters import time_to_seconds


def track_markup(_, videoid, user_id, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
                style="success"          # Green
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
                style="primary"          # Blue
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style="danger"           # Red
            )
        ],
    ]
    return buttons


def stream_markup_timer(_, chat_id, played, dur):
    # ... (progress bar code আগের মতোই রাখো)

    buttons = [
        [
            InlineKeyboardButton(
                text=f"{played} {bar} {dur}",
                callback_data="GetTimer"
            )
        ],
        [
            InlineKeyboardButton(text="▶️ Resume", callback_data=f"ADMIN Resume|{chat_id}", style="success"),
            InlineKeyboardButton(text="⏸ Pause", callback_data=f"ADMIN Pause|{chat_id}", style="primary"),
            InlineKeyboardButton(text="🔄 Replay", callback_data=f"ADMIN Replay|{chat_id}"),
            InlineKeyboardButton(text="⏭ Skip", callback_data=f"ADMIN Skip|{chat_id}", style="primary"),
            InlineKeyboardButton(text="⏹ Stop", callback_data=f"ADMIN Stop|{chat_id}", style="danger"),
        ],
    ]
    return buttons


def stream_markup(_, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="▶️", callback_data=f"ADMIN Resume|{chat_id}", style="success"),
            InlineKeyboardButton(text="⏸", callback_data=f"ADMIN Pause|{chat_id}", style="primary"),
            InlineKeyboardButton(text="🔄", callback_data=f"ADMIN Replay|{chat_id}"),
            InlineKeyboardButton(text="⏭", callback_data=f"ADMIN Skip|{chat_id}", style="primary"),
            InlineKeyboardButton(text="⏹", callback_data=f"ADMIN Stop|{chat_id}", style="danger"),
        ],
    ]
    return buttons


# বাকি ফাংশনগুলো (playlist, livestream, slider) একইভাবে আপডেট করো
def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(text=_["P_B_1"], callback_data=..., style="success"),
            InlineKeyboardButton(text=_["P_B_2"], callback_data=..., style="primary"),
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=..., style="danger"),
        ],
    ]
    return buttons