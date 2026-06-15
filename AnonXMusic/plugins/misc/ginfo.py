'''
Plugin : Users/Group Info.
Author: Rehanna
Usage: Sudo users can send /id to get users data & /ginfo -100xxx to get group info.
'''

from pyrogram import filters
from pyrogram.types import Message
from AnonXMusic import app
from AnonXMusic.misc import SUDOERS


@app.on_message(filters.command("ginfo") & SUDOERS)
async def groupinfo(client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text("<b>Usage:</b> /ginfo [GROUP_ID/USERNAME]")

    group_identifier = message.command[1]

    try:
        try:
            group = await client.get_chat(group_identifier)
        except Exception as e:
            if "PEER_ID_INVALID" in str(e):
                return await message.reply_text("I can't access this group. Make sure I am admin in this group.")
            return await message.reply_text(f"An error occurred: {str(e)}")

        if str(group.type) not in ["SUPERGROUP", "GROUP"]:
            return await message.reply_text("This is not a group!")

        # Get group information
        try:
            members_count = await app.get_chat_members_count(group.id)
        except:
            members_count = "Unknown"

        description = group.description or "No description available"
        username = f"@{group.username}" if group.username else "Private Group"

        # Owner info
        owner_username = "Unknown"
        owner_id = "Unknown"
        try:
            if hasattr(group, 'creator') and group.creator:
                owner = await app.get_chat_member(group.id, group.creator.id)
                owner_username = f"@{owner.user.username}" if owner.user.username else "Unknown"
                owner_id = owner.user.id
        except:
            pass

        # Bots & Zombies count
        bots_count = 0
        zombies_count = 0
        try:
            async for member in app.get_chat_members(group.id, limit=500):
                if member.user.is_bot:
                    bots_count += 1
                if member.user.is_deleted:
                    zombies_count += 1
        except:
            pass

        info_text = f"📊 **Group Information**\n\n"
        info_text += f"**Title:** {group.title}\n"
        info_text += f"**ID:** <code>{group.id}</code>\n"
        info_text += f"**Username:** {username}\n"
        info_text += f"**Members:** {members_count}\n"
        info_text += f"**Description:** {description}\n"
        info_text += f"**Owner:** {owner_username} (<code>{owner_id}</code>)\n"
        info_text += f"**Bots:** {bots_count}\n"
        info_text += f"**Zombies:** {zombies_count}\n"

        if group.invite_link:
            info_text += f"**Invite Link:** {group.invite_link}\n"

        await message.reply_text(info_text)

    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")


# ================== USER INFO ==================
@app.on_message(filters.command(['id', 'me', 'info']))
async def user_info(client, message: Message):
    replied_user = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    
    if not replied_user:
        return await message.reply_text("Cannot retrieve user information.")

    user_id = replied_user.id
    username = f"@{replied_user.username}" if replied_user.username else "No Username"
    first_name = replied_user.first_name or "Unknown"
    last_name = replied_user.last_name or ""
    full_name = f"{first_name} {last_name}".strip()

    info_text = f"👤 **User Information**\n\n"
    info_text += f"**User ID:** <code>{user_id}</code>\n"
    info_text += f"**Name:** {full_name}\n"
    info_text += f"**Username:** {username}\n"
    info_text += f"**Is Bot:** {'Yes' if replied_user.is_bot else 'No'}\n"
    info_text += f"**Is Premium:** {'Yes' if replied_user.is_premium else 'No'}\n"

    await message.reply_text(info_text)