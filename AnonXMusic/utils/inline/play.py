# Copyright (c) 2026 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

import math
from pyrogram import enums, types
from AnonXMusic.utils.formatters import time_to_seconds

# Style definitions map
STYLES = {
    "default": enums.ButtonStyle.DEFAULT,
    "primary": enums.ButtonStyle.PRIMARY,
    "success": enums.ButtonStyle.SUCCESS,
    "danger": enums.ButtonStyle.DANGER,
    "status": enums.ButtonStyle.DEFAULT,
    "nav": enums.ButtonStyle.DEFAULT,
    "link": enums.ButtonStyle.DEFAULT,
    "menu": enums.ButtonStyle.PRIMARY,
    "media": enums.ButtonStyle.PRIMARY,
    "play": enums.ButtonStyle.SUCCESS,
    "setting": enums.ButtonStyle.PRIMARY,
    "enabled": enums.ButtonStyle.SUCCESS,
    "disabled": enums.ButtonStyle.DANGER,
}

def _button(text: str, category: str = "default", **kwargs):
    return types.InlineKeyboardButton(
        text=text,
        style=STYLES.get(category, enums.ButtonStyle.DEFAULT),
        **kwargs,
    )

def track_markup(_, videoid, user_id, channel, fplay) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(
        [
            [
                _button(text=_["P_B_1"], category="success", callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}"),
                _button(text=_["P_B_2"], category="primary", callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}")
            ],
            [
                _button(text=_["CLOSE_BUTTON"], category="danger", callback_data=f"forceclose {videoid}|{user_id}")
            ]
        ]
    )

def stream_markup_timer(_, chat_id, played, dur) -> types.InlineKeyboardMarkup:
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    percentage = (played_sec / duration_sec) * 100 if duration_sec > 0 else 0
    umm = min(math.floor(percentage / 10), 9)

    bar_list = ["—"] * 10
    bar_list[umm] = "◉"
    bar = "".join(bar_list)

    return types.InlineKeyboardMarkup(
        [
            [
                _button(text=f"{played} {bar} {dur}", category="status", callback_data="GetTimer")
            ],
            [   
                _button(text="▷", category="success", callback_data=f"ADMIN Resume|{chat_id}"),
                _button(text="II", category="primary", callback_data=f"ADMIN Pause|{chat_id}"),
                _button(text="↻", category="default", callback_data=f"ADMIN Replay|{chat_id}"),
                _button(text="‣‣I", category="primary", callback_data=f"ADMIN Skip|{chat_id}"),
                _button(text="▢", category="danger", callback_data=f"ADMIN Stop|{chat_id}")
            ]
        ]
    )

def stream_markup(_, chat_id) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(
        [
            [
                _button(text="▷", category="success", callback_data=f"ADMIN Resume|{chat_id}"),
                _button(text="II", category="primary", callback_data=f"ADMIN Pause|{chat_id}"),
                _button(text="↻", category="default", callback_data=f"ADMIN Replay|{chat_id}"),
                _button(text="‣‣I", category="primary", callback_data=f"ADMIN Skip|{chat_id}"),
                _button(text="▢", category="danger", callback_data=f"ADMIN Stop|{chat_id}")
            ]
        ]
    )

def playlist_markup(_, videoid, user_id, ptype, channel, fplay) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(
        [
            [
                _button(text=_["P_B_1"], category="success", callback_data=f"AnonyPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}"),
                _button(text=_["P_B_2"], category="primary", callback_data=f"AnonyPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}")
            ],
            [
                _button(text=_["CLOSE_BUTTON"], category="danger", callback_data=f"forceclose {videoid}|{user_id}")
            ]
        ]
    )

def livestream_markup(_, videoid, user_id, mode, channel, fplay) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(
        [
            [
                _button(text=_["P_B_3"], category="success", callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}")
            ],
            [
                _button(text=_["CLOSE_BUTTON"], category="danger", callback_data=f"forceclose {videoid}|{user_id}")
            ]
        ]
    )

def slider_markup(_, videoid, user_id, query, query_type, channel, fplay) -> types.InlineKeyboardMarkup:
    query = f"{query[:20]}"
    return types.InlineKeyboardMarkup(
        [
            [
                _button(text=_["P_B_1"], category="success", callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}"),
                _button(text=_["P_B_2"], category="primary", callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}")
            ],
            [
                _button(text="◁", category="default", callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}"),
                _button(text=_["CLOSE_BUTTON"], category="danger", callback_data=f"forceclose {query}|{user_id}"),
                _button(text="▷", category="default", callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}")
            ]
        ]
    )