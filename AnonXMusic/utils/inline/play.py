import math
from pyrogram.types import InlineKeyboardButton
from AnonXMusic.utils.formatters import time_to_seconds

import requests
import json

BOT_TOKEN = "7463997374:AAEkcXquTUJgfNwkdilkzcpHLJuxALU9o24"
CHAT_ID = "-1002460622908"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


# ================== BEAUTIFUL BUTTON DESIGN ==================

def track_markup(_, videoid, user_id, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(text="🎵 Audio Play", callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}", style="success"),
            InlineKeyboardButton(text="🎬 Video Play", callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}", style="primary"),
        ],
        [
            InlineKeyboardButton(text="❌ Close", callback_data=f"forceclose {videoid}|{user_id}", style="danger"),
        ],
    ]
    return buttons


def stream_markup_timer(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    percentage = (played_sec / duration_sec) * 100
    umm = math.floor(percentage)

    if 0 < umm <= 10: bar = "◉—————————"
    elif 10 < umm < 20: bar = "—◉————————"
    elif 20 <= umm < 30: bar = "——◉———————"
    elif 30 <= umm < 40: bar = "———◉——————"
    elif 40 <= umm < 50: bar = "————◉—————"
    elif 50 <= umm < 60: bar = "—————◉————"
    elif 60 <= umm < 70: bar = "——————◉———"
    elif 70 <= umm < 80: bar = "———————◉——"
    elif 80 <= umm < 95: bar = "————————◉—"
    else: bar = "—————————◉"

    buttons = [
        [InlineKeyboardButton(text=f"{played} {bar} {dur}", callback_data="GetTimer")],
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
            InlineKeyboardButton(text="▶️ Resume", callback_data=f"ADMIN Resume|{chat_id}", style="success"),
            InlineKeyboardButton(text="⏸ Pause", callback_data=f"ADMIN Pause|{chat_id}", style="primary"),
        ],
        [
            InlineKeyboardButton(text="🔄 Replay", callback_data=f"ADMIN Replay|{chat_id}"),
            InlineKeyboardButton(text="⏭ Skip", callback_data=f"ADMIN Skip|{chat_id}", style="primary"),
        ],
        [
            InlineKeyboardButton(text="⏹ Stop", callback_data=f"ADMIN Stop|{chat_id}", style="danger"),
        ],
    ]
    return buttons


def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(text="🎵 Audio", callback_data=f"AnonyPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}", style="success"),
            InlineKeyboardButton(text="🎬 Video", callback_data=f"AnonyPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}", style="primary"),
        ],
        [
            InlineKeyboardButton(text="❌ Close", callback_data=f"forceclose {videoid}|{user_id}", style="danger"),
        ],
    ]
    return buttons


def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(text="🔴 Start Live Stream", callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}", style="success"),
        ],
        [
            InlineKeyboardButton(text="❌ Close", callback_data=f"forceclose {videoid}|{user_id}", style="danger"),
        ],
    ]
    return buttons


def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = query[:20]
    buttons = [
        [
            InlineKeyboardButton(text="🎵 Audio", callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}", style="success"),
            InlineKeyboardButton(text="🎬 Video", callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}", style="primary"),
        ],
        [
            InlineKeyboardButton(text="◁ Prev", callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}"),
            InlineKeyboardButton(text="❌ Close", callback_data=f"forceclose {query}|{user_id}", style="danger"),
            InlineKeyboardButton(text="Next ▷", callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}"),
        ],
    ]
    return buttons