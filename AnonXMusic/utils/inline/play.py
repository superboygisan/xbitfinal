import math

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from AnonXMusic.utils.formatters import time_to_seconds


# =========================================================
# COLOR BUTTON BUILDER
# =========================================================

def build_keyboard(data):

    rows = []

    for row in data["inline_keyboard"]:

        buttons = []

        for btn in row:

            text = btn["text"]
            style = btn.get("style")

            # Fake Telegram Colors

            if style == "primary":
                text = f"🔵 {text}"

            elif style == "success":
                text = f"🟢 {text}"

            elif style == "danger":
                text = f"🔴 {text}"

            elif style == "warning":
                text = f"🟡 {text}"

            elif style == "purple":
                text = f"🟣 {text}"

            # URL BUTTON

            if "url" in btn:

                buttons.append(
                    InlineKeyboardButton(
                        text=text,
                        url=btn["url"]
                    )
                )

            # USER BUTTON

            elif "user_id" in btn:

                buttons.append(
                    InlineKeyboardButton(
                        text=text,
                        user_id=btn["user_id"]
                    )
                )

            # CALLBACK BUTTON

            else:

                buttons.append(
                    InlineKeyboardButton(
                        text=text,
                        callback_data=btn["callback_data"]
                    )
                )

        rows.append(buttons)

    return InlineKeyboardMarkup(rows)


# =========================================================
# TRACK MARKUP
# =========================================================

def track_markup(_, videoid, user_id, channel, fplay):

    buttons = {
        "inline_keyboard": [
            [
                {
                    "text": f"🌛 {_['P_B_1']}",
                    "callback_data": f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
                    "style": "success"
                },
                {
                    "text": f"🌛 {_['P_B_2']}",
                    "callback_data": f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
                    "style": "primary"
                },
            ],
            [
                {
                    "text": f"🌛 {_['CLOSE_BUTTON']}",
                    "callback_data": f"forceclose {videoid}|{user_id}",
                    "style": "danger"
                }
            ],
        ]
    }

    return build_keyboard(buttons)


# =========================================================
# STREAM MARKUP TIMER
# =========================================================

def stream_markup_timer(_, chat_id, played, dur):

    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)

    percentage = (played_sec / duration_sec) * 100
    umm = math.floor(percentage)

    # 🌛 Animated Processing Bar

    if 0 < umm <= 10:
        progress = "🌛◉─────────"

    elif 10 < umm < 20:
        progress = "─🌛◉────────"

    elif 20 <= umm < 30:
        progress = "──🌛◉───────"

    elif 30 <= umm < 40:
        progress = "───🌛◉──────"

    elif 40 <= umm < 50:
        progress = "────🌛◉─────"

    elif 50 <= umm < 60:
        progress = "─────🌛◉────"

    elif 60 <= umm < 70:
        progress = "──────🌛◉───"

    elif 70 <= umm < 80:
        progress = "───────🌛◉──"

    elif 80 <= umm < 95:
        progress = "────────🌛◉─"

    else:
        progress = "─────────🌛◉"

    buttons = {
        "inline_keyboard": [

            [
                {
                    "text": progress,
                    "callback_data": "progress",
                    "style": "primary"
                }
            ],

            [
                {
                    "text": "▶️",
                    "callback_data": f"ADMIN Resume|{chat_id}",
                    "style": "success"
                },
                {
                    "text": "⏸",
                    "callback_data": f"ADMIN Pause|{chat_id}",
                    "style": "warning"
                },
                {
                    "text": "↻",
                    "callback_data": f"ADMIN Replay|{chat_id}",
                    "style": "primary"
                },
                {
                    "text": "⏭",
                    "callback_data": f"ADMIN Skip|{chat_id}",
                    "style": "purple"
                },
                {
                    "text": "⏹",
                    "callback_data": f"ADMIN Stop|{chat_id}",
                    "style": "danger"
                }
            ]
        ]
    }

    return build_keyboard(buttons)


# =========================================================
# STREAM MARKUP
# =========================================================

def stream_markup(_, chat_id):

    buttons = {
        "inline_keyboard": [
            [
                {
                    "text": "▶️",
                    "callback_data": f"ADMIN Resume|{chat_id}",
                    "style": "success"
                },
                {
                    "text": "⏸",
                    "callback_data": f"ADMIN Pause|{chat_id}",
                    "style": "warning"
                },
                {
                    "text": "↻",
                    "callback_data": f"ADMIN Replay|{chat_id}",
                    "style": "primary"
                },
                {
                    "text": "⏭",
                    "callback_data": f"ADMIN Skip|{chat_id}",
                    "style": "purple"
                },
                {
                    "text": "⏹",
                    "callback_data": f"ADMIN Stop|{chat_id}",
                    "style": "danger"
                }
            ]
        ]
    }

    return build_keyboard(buttons)


# =========================================================
# PLAYLIST MARKUP
# =========================================================

def playlist_markup(_, videoid, user_id, ptype, channel, fplay):

    buttons = {
        "inline_keyboard": [
            [
                {
                    "text": f"🌛 {_['P_B_1']}",
                    "callback_data": f"AnonyPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
                    "style": "success"
                },
                {
                    "text": f"🌛 {_['P_B_2']}",
                    "callback_data": f"AnonyPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
                    "style": "primary"
                },
            ],
            [
                {
                    "text": f"🌛 {_['CLOSE_BUTTON']}",
                    "callback_data": f"forceclose {videoid}|{user_id}",
                    "style": "danger"
                },
            ],
        ]
    }

    return build_keyboard(buttons)


# =========================================================
# LIVESTREAM MARKUP
# =========================================================

def livestream_markup(_, videoid, user_id, mode, channel, fplay):

    buttons = {
        "inline_keyboard": [
            [
                {
                    "text": f"🌛 {_['P_B_3']}",
                    "callback_data": f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
                    "style": "success"
                },
            ],
            [
                {
                    "text": f"🌛 {_['CLOSE_BUTTON']}",
                    "callback_data": f"forceclose {videoid}|{user_id}",
                    "style": "danger"
                },
            ],
        ]
    }

    return build_keyboard(buttons)


# =========================================================
# SLIDER MARKUP
# =========================================================

def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):

    query = f"{query[:20]}"

    buttons = {
        "inline_keyboard": [
            [
                {
                    "text": f"🌛 {_['P_B_1']}",
                    "callback_data": f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
                    "style": "success"
                },
                {
                    "text": f"🌛 {_['P_B_2']}",
                    "callback_data": f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
                    "style": "primary"
                },
            ],
            [
                {
                    "text": "◁",
                    "callback_data": f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
                    "style": "primary"
                },
                {
                    "text": f"🌛 {_['CLOSE_BUTTON']}",
                    "callback_data": f"forceclose {query}|{user_id}",
                    "style": "danger"
                },
                {
                    "text": "▷",
                    "callback_data": f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
                    "style": "primary"
                },
            ],
        ]
    }

    return build_keyboard(buttons)