import asyncio
import importlib

from pyrogram import idle

import config

from AnonXMusic import LOGGER, app, userbot
from AnonXMusic.core.call import Anony
from AnonXMusic.misc import sudo
from AnonXMusic.plugins import ALL_MODULES
from AnonXMusic.utils.database import (
    get_banned_users,
    get_gbanned,
)

from config import BANNED_USERS


async def init():

    # ---------------- ASSISTANT CHECK ----------------
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error(
            "Assistant client variables not defined, exiting..."
        )
        exit()

    # ---------------- LOAD SUDO ----------------
    await sudo()

    # ---------------- LOAD BANNED USERS ----------------
    try:

        users = await get_gbanned()

        for user_id in users:
            BANNED_USERS.add(user_id)

        users = await get_banned_users()

        for user_id in users:
            BANNED_USERS.add(user_id)

    except Exception as e:
        print(f"BANNED LOAD ERROR: {e}")

    # ---------------- START BOT ----------------
    await app.start()

    LOGGER("AnonXMusic").info(
        "Main Bot Started Successfully!"
    )

    # ---------------- IMPORT MODULES ----------------
    for all_module in ALL_MODULES:

        importlib.import_module(
            "AnonXMusic.plugins" + all_module
        )

    LOGGER("AnonXMusic.plugins").info(
        "Successfully Imported All Modules!"
    )

    # ---------------- START USERBOT ----------------
    try:

        await userbot.start()

        LOGGER("AnonXMusic").info(
            "Assistant Started Successfully!"
        )

    except Exception as e:

        LOGGER("AnonXMusic").error(
            f"Assistant Start Error : {e}"
        )

    # ---------------- START PYTGCALLS ----------------
    try:

        await Anony.start()

        LOGGER("AnonXMusic").info(
            "Voice Call Client Started!"
        )

    except Exception as e:

        LOGGER("AnonXMusic").error(
            f"PyTgCalls Error : {e}"
        )

    # ---------------- LOAD DECORATORS ----------------
    try:

        await Anony.decorators()

        LOGGER("AnonXMusic").info(
            "Decorators Loaded Successfully!"
        )

    except Exception as e:

        LOGGER("AnonXMusic").error(
            f"Decorator Error : {e}"
        )

    # ---------------- BOT ONLINE ----------------
    LOGGER("AnonXMusic").info(
        "AnonX Music Bot Started Successfully!"
    )

    # ---------------- IDLE ----------------
    await idle()

    # ---------------- STOP BOT ----------------
    await app.stop()

    LOGGER("AnonXMusic").info(
        "Stopping AnonX Music Bot..."
    )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())