import time
import re
import random
import asyncio
import traceback

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate
from pyrogram.errors.exceptions.flood_420 import SlowmodeWait
from ytSearch import VideosSearch

import config
from AnonXMusic import app
from AnonXMusic.misc import _boot_
from AnonXMusic.plugins.sudo.sudoers import sudoers_list
from AnonXMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
    blacklist_chat,
)
from AnonXMusic.utils.decorators.language import LanguageStart
from AnonXMusic.utils.formatters import get_readable_time

# Absolute import connection fixed
from AnonXMusic.utils.inline.start import private_panel, start_panel

from config import BANNED_USERS, LOGGER_ID
from strings import get_string


def make_panel_compact(original_markup):
    if not original_markup:
        return None

    if hasattr(original_markup, "inline_keyboard"):
        raw_keyboard = original_markup.inline_keyboard
    elif isinstance(original_markup, list):
        raw_keyboard = original_markup
    else:
        return original_markup

    new_keyboard = []
    current_row = []

    for row in raw_keyboard:
        for button in row:
            if not button:
                continue

            if isinstance(button, dict):
                btn_text = button.get("text", "")
                btn_url = button.get("url")
                btn_cb = button.get("callback_data")
            else:
                btn_text = getattr(button, "text", "")
                btn_url = getattr(button, "url", None)
                btn_cb = getattr(button, "callback_data", None)

            clean_text = str(btn_text).strip("• ").strip("⌗ ")
            kwargs = {}

            if btn_url:
                kwargs["url"] = btn_url
            elif btn_cb:
                kwargs["callback_data"] = btn_cb
            else:
                kwargs["callback_data"] = "noop"

            new_btn = InlineKeyboardButton(text=clean_text, **kwargs)

            if "ADD ME" in clean_text.upper():
                if current_row:
                    new_keyboard.append(current_row)
                    current_row = []
                new_keyboard.append([new_btn])
            else:
                current_row.append(new_btn)
                if len(current_row) == 2:
                    new_keyboard.append(current_row)
                    current_row = []

    if current_row:
        new_keyboard.append(current_row)

    return InlineKeyboardMarkup(new_keyboard)


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):

    await add_served_user(message.from_user.id)

    # ---------------- STICKER ----------------
    try:
        await message.reply_sticker(
            "CAACAgUAAx0CdQO5IgACMTplUFOpwDjf-UC7pqVt9uG659qxWQACfQkAAghYGFVtSkRZ5FZQXDME"
        )
    except Exception as e:
        print("Sticker Error:", e)

    await asyncio.sleep(0.5)

    # ---------------- BUTTONS PARSING (FIXED CONNECTION) ----------------
    try:
        # Pass app.username instead of language string object to fix crash
        raw_buttons = private_panel(app.username)
        out = make_panel_compact(raw_buttons)
    except Exception as e:
        print(f"BUTTON COMPACT ERROR: {e}")
        try:
            out = InlineKeyboardMarkup(private_panel(app.username))
        except:
            out = None

    # ---------------- MEDIA ----------------
    try:
        media_url = random.choice(config.START_IMG_URL)
    except:
        media_url = None

    # ---------------- SEND EXECUTION ----------------
    try:
        if media_url and str(media_url).endswith(".mp4"):
            await message.reply_video(
                video=media_url,
                caption=_["start_2"].format(
                    message.from_user.mention,
                    app.mention
                ),
                reply_markup=out,
            )
        elif media_url:
            await message.reply_photo(
                photo=media_url,
                caption=_["start_2"].format(
                    message.from_user.mention,
                    app.mention
                ),
                reply_markup=out,
            )
        else:
            await message.reply_text(
                text=_["start_2"].format(
                    message.from_user.mention,
                    app.mention
                ),
                reply_markup=out,
                disable_web_page_preview=True,
            )

    except Exception as e:
        print(f"START MEDIA ERROR: {e}")
        try:
            await message.reply_text(
                text=_["start_2"].format(
                    message.from_user.mention,
                    app.mention
                ),
                reply_markup=out,
                disable_web_page_preview=True,
            )
        except Exception as ex:
            print(f"CRITICAL FALLBACK START FAILED: {ex}")

    # ---------------- LOGGER ----------------
    if await is_on_off(2):
        try:
            await app.send_message(
                chat_id=config.LOGGER_ID,
                text=f"{message.from_user.mention} started the bot.\n\n"
                     f"User ID : {message.from_user.id}\n"
                     f"Username : @{message.from_user.username}",
            )
        except:
            pass


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):

    try:
        # Pass app.username here as well to keep group panel safe
        out = make_panel_compact(start_panel(app.username))
    except:
        out = InlineKeyboardMarkup(start_panel(app.username))
        
    uptime = int(time.time() - _boot_)

    try:
        media_url = random.choice(config.START_IMG_URL)
    except:
        media_url = None

    try:
        if media_url and str(media_url).endswith(".mp4"):
            await message.reply_video(
                video=media_url,
                caption=_["start_1"].format(
                    app.mention,
                    get_readable_time(uptime)
                ),
                reply_markup=out,
            )
        elif media_url:
            await message.reply_photo(
                photo=media_url,
                caption=_["start_1"].format(
                    app.mention,
                    get_readable_time(uptime)
                ),
                reply_markup=out,
            )
        else:
            await message.reply_text(
                text=_["start_1"].format(
                    app.mention,
                    get_readable_time(uptime)
                ),
                reply_markup=out,
            )

        return await add_served_chat(message.chat.id)

    except ChannelPrivate:
        return

    except SlowmodeWait as e:
        await asyncio.sleep(e.value)

    except Exception as e:
        print(f"GROUP START ERROR: {e}")