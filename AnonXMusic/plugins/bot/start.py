import time
import re
import random
import asyncio

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate
from pyrogram.errors.exceptions.flood_420 import SlowmodeWait

from AnonXMusic import app
from AnonXMusic.misc import _boot_
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
from AnonXMusic.utils.inline import private_panel, start_panel, help_pannel

from config import BANNED_USERS, LOGGER_ID, START_IMG_URL, SUPPORT_CHAT
from strings import get_string


# ---------------- CLEAN BUTTON FIX ----------------
def make_panel_compact(original_markup):
    if not original_markup:
        return None

    raw_keyboard = getattr(original_markup, "inline_keyboard", original_markup)

    new_keyboard = []
    current_row = []

    for row in raw_keyboard:
        for button in row:

            text = getattr(button, "text", button.get("text", "")).strip("• ").strip("⌗ ")

            kwargs = {}

            url = getattr(button, "url", None) or button.get("url")
            cb = getattr(button, "callback_data", None) or button.get("callback_data")

            if url:
                kwargs["url"] = url
            elif cb:
                kwargs["callback_data"] = cb
            else:
                kwargs["callback_data"] = "noop"

            new_btn = InlineKeyboardButton(text=text, **kwargs)

            if "ADD ME" in text.upper() or "SOURCE" in text.upper():
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


# ---------------- PRIVATE START ----------------
@app.on_message(filters.command("start") & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):

    await add_served_user(message.from_user.id)

    args = message.text.split()

    # ---------- HELP MODE ----------
    if len(args) > 1 and args[1].startswith("help"):
        keyboard = make_panel_compact(help_pannel(_))

        media_url = random.choice(START_IMG_URL)

        if str(media_url).endswith(".mp4"):
            await message.reply_video(
                video=media_url,
                caption=_["help_1"].format(SUPPORT_CHAT),
                reply_markup=keyboard
            )
        else:
            await message.reply_photo(
                photo=media_url,
                caption=_["help_1"].format(SUPPORT_CHAT),
                reply_markup=keyboard
            )
        return

    # ---------- SUDO MODE ----------
    if len(args) > 1 and args[1].startswith("sud"):
        return

    # ---------- INFO MODE ----------
    if len(args) > 1 and args[1].startswith("inf"):
        return

    # ---------- NORMAL START ----------
    keyboard = make_panel_compact(private_panel(_))
    media_url = random.choice(START_IMG_URL)

    try:
        if str(media_url).endswith(".mp4"):
            await message.reply_video(
                video=media_url,
                caption=_["start_2"].format(message.from_user.mention, app.mention),
                reply_markup=keyboard,
            )
        else:
            await message.reply_photo(
                photo=media_url,
                caption=_["start_2"].format(message.from_user.mention, app.mention),
                reply_markup=keyboard,
            )

    except Exception:
        await message.reply_text(
            text=_["start_2"].format(message.from_user.mention, app.mention),
            reply_markup=keyboard
        )

    # ---------- LOGGER ----------
    if await is_on_off(2):
        await app.send_message(
            LOGGER_ID,
            f"{message.from_user.mention} started bot\nUser ID: {message.from_user.id}"
        )


# ---------------- GROUP START ----------------
@app.on_message(filters.command("start") & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):

    keyboard = make_panel_compact(start_panel(_))
    uptime = int(time.time() - _boot_)
    media_url = random.choice(START_IMG_URL)

    try:
        if str(media_url).endswith(".mp4"):
            await message.reply_video(
                video=media_url,
                caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
                reply_markup=keyboard,
            )
        else:
            await message.reply_photo(
                photo=media_url,
                caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
                reply_markup=keyboard,
            )

        await add_served_chat(message.chat.id)

    except ChannelPrivate:
        return

    except SlowmodeWait as e:
        await asyncio.sleep(e.value)
        return


# ---------------- WELCOME ----------------
@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):

    for member in message.new_chat_members:

        try:
            if await is_banned_user(member.id):
                await message.chat.ban_member(member.id)

            if member.id == app.id:

                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text("Please use supergroup.")
                    return await app.leave_chat(message.chat.id)

                if message.chat.id in await blacklisted_chats():
                    await message.reply_text("This group is blacklisted.")
                    return await app.leave_chat(message.chat.id)

                keyboard = make_panel_compact(start_panel(_))
                media_url = random.choice(START_IMG_URL)

                if str(media_url).endswith(".mp4"):
                    await message.reply_video(
                        video=media_url,
                        caption=_["start_3"].format(
                            member.first_name,
                            app.mention,
                            message.chat.title,
                            app.mention
                        ),
                        reply_markup=keyboard,
                    )
                else:
                    await message.reply_photo(
                        photo=media_url,
                        caption=_["start_3"].format(
                            member.first_name,
                            app.mention,
                            message.chat.title,
                            app.mention
                        ),
                        reply_markup=keyboard,
                    )

                await add_served_chat(message.chat.id)
                await message.stop_propagation()

        except Exception as e:
            print("WELCOME ERROR:", e)