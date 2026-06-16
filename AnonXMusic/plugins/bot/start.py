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

from AnonXMusic.utils.inline import private_panel, start_panel, help_pannel

from config import BANNED_USERS, LOGGER_ID
from strings import get_string


def make_panel_compact(original_markup):
    if not original_markup:
        return None

    raw_keyboard = []
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
            if isinstance(button, dict):
                btn_text = button.get("text", "")
                btn_url = button.get("url")
                btn_cb = button.get("callback_data")
                btn_siq = button.get("switch_inline_query")
                btn_siqc = button.get("switch_inline_query_current_chat")
            else:
                btn_text = getattr(button, "text", "")
                btn_url = getattr(button, "url", None)
                btn_cb = getattr(button, "callback_data", None)
                btn_siq = getattr(button, "switch_inline_query", None)
                btn_siqc = getattr(button, "switch_inline_query_current_chat", None)

            clean_text = btn_text.strip("• ").strip("⌗ ")
            
            # CRITICAL FIX: Safe construction parameter to bypass NoneType writing errors
            kwargs = {}
            if btn_url:
                kwargs["url"] = str(btn_url)
            elif btn_cb:
                kwargs["callback_data"] = str(btn_cb)
            elif btn_siq is not None:
                kwargs["switch_inline_query"] = str(btn_siq)
            elif btn_siqc is not None:
                kwargs["switch_inline_query_current_chat"] = str(btn_siqc)
            else:
                # Fallback safeguard button to satisfy raw vector compilation
                kwargs["callback_data"] = "noop"

            new_btn = InlineKeyboardButton(text=clean_text, **kwargs)

            if "ADD ME" in clean_text.upper() or "SOURCE" in clean_text.upper():
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
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = make_panel_compact(help_pannel(_))
            await message.reply_sticker("CAACAgUAAx0CdQO5IgACMTplUFOpwDjf-UC7pqVt9uG659qxWQACfQkAAghYGFVtSkRZ5FZQXDME")

            media_url = random.choice(config.START_IMG_URL)
            try:
                if str(media_url).endswith(".mp4"):
                    return await message.reply_video(video=media_url, caption=_["help_1"].format(config.SUPPORT_CHAT), reply_markup=keyboard, has_spoiler=True)
                else:
                    return await message.reply_photo(photo=media_url, caption=_["help_1"].format(config.SUPPORT_CHAT), reply_markup=keyboard, has_spoiler=True)
            except Exception as e:
                print(f"Help Media Error: {e}")
                return await message.reply_text(text=_["help_1"].format(config.SUPPORT_CHAT), reply_markup=keyboard)

        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
            return
        if name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                        InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                    ],
                ]
            )
            await m.delete()
            try:
                await app.send_photo(chat_id=message.chat.id, photo=thumbnail, caption=searched_text, reply_markup=key)
            except:
                await app.send_message(chat_id=message.chat.id, text=searched_text, reply_markup=key)
    else:
        await message.reply_sticker("CAACAgUAAx0CdQO5IgACMTplUFOpwDjf-UC7pqVt9uG659qxWQACfQkAAghYGFVtSkRZ5FZQXDME")

        out = make_panel_compact(private_panel(_))
        media_url = random.choice(config.START_IMG_URL)

        try:
            if str(media_url).endswith(".mp4"):
                await message.reply_video(
                    video=media_url,
                    caption=_["start_2"].format(message.from_user.mention, app.mention),
                    reply_markup=out,
                    has_spoiler=True,
                )
            else:
                await message.reply_photo(
                    photo=media_url,
                    caption=_["start_2"].format(message.from_user.mention, app.mention),
                    reply_markup=out,
                    has_spoiler=True,
                )
        except Exception as e:
            print(f"START PM MEDIA GLITCH: {e}")
            await message.reply_text(
                text=_["start_2"].format(message.from_user.mention, app.mention),
                reply_markup=out,
                disable_web_page_preview=True
            )

        if await is_on_off(2):
            return await app.send_message(
                chat_id=config.LOGGER_ID,
                text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
            )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = make_panel_compact(start_panel(_))
    uptime = int(time.time() - _boot_)
    media_url = random.choice(config.START_IMG_URL)
    try:
        if str(media_url).endswith(".mp4"):
            await message.reply_video(video=media_url, caption=_["start_1"].format(app.mention, get_readable_time(uptime)), reply_markup=out, has_spoiler=True)
        else:
            await message.reply_photo(photo=media_url, caption=_["start_1"].format(app.mention, get_readable_time(uptime)), reply_markup=out, has_spoiler=True)
        return await add_served_chat(message.chat.id)
    except ChannelPrivate:
        return
    except SlowmodeWait as e:
        await asyncio.sleep(e.value)
        try:
            if str(media_url).endswith(".mp4"):
                await message.reply_video(video=media_url, caption=_["start_1"].format(app.mention, get_readable_time(uptime)), reply_markup=out, has_spoiler=True)
            else:
                await message.reply_photo(photo=media_url, caption=_["start_1"].format(app.mention, get_readable_time(uptime)), reply_markup=out, has_spoiler=True)
            return await add_served_chat(message.chat.id)
        except:
            return


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                ch = await app.get_chat(message.chat.id)
                if (ch.title and re.search(r'[\u1000-\u109F]', ch.title)) or \
                    (ch.description and re.search(r'[\u1000-\u109F]', ch.description)):
                        await blacklist_chat(message.chat.id)
                        await message.reply_text("This group is not allowed to play songs")
                        await app.send_message(LOGGER_ID, f"This group has been blacklisted automatically due to myanmar characters in the chat title, description or message \n Title:{ch.title} \n ID:{message.chat.id}")
                        return await app.leave_chat(message.chat.id)

                out = make_panel_compact(start_panel(_))
                media_url = random.choice(config.START_IMG_URL)
                if str(media_url).endswith(".mp4"):
                    await message.reply_video(video=media_url, caption=_["start_3"].format(message.from_user.first_name, app.mention, message.chat.title, app.mention), reply_markup=out, has_spoiler=True)
                else:
                    await message.reply_photo(photo=media_url, caption=_["start_3"].format(message.from_user.first_name, app.mention, message.chat.title, app.mention), reply_markup=out, has_spoiler=True)
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)