import asyncio
from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message, User

from datetime import datetime
from AnonXMusic import app
from AnonXMusic.utils.custom_filters import command
from AnonXMusic.supports import get_support_staff
from AnonXMusic.database.antispam_db import GBan
from AnonXMusic.utils import get_readable_time
from AnonXMusic.utils.database import get_served_chats
from AnonXMusic.utils.extract_user import extract_user
from AnonXMusic.utils.decorators.language import language
from config import BANNED_USERS
from strings import helpers

db = GBan()
SUPPORT_STAFF = get_support_staff()

@app.on_message(command(["gban", "globalban"], sudo_cmd=True))
@language
async def global_ban(client, message: Message, _):
    if len(message.text.split()) == 1:
        return await message.reply_text(_["general_1"])
        
    if len(message.text.split()) == 2 and not message.reply_to_message:
        return await message.reply_text("Please enter a reason to gban the user!")
        
    user_id, user_first_name, user_name = await extract_user(client, message)
    if user_id == message.from_user.id:
        return await message.reply_text(_["gban_1"])
    elif user_id == client.id:
        return await message.reply_text(_["gban_2"])
    elif user_id in SUPPORT_STAFF:
        return await message.reply_text(_["gban_3"])

    gban_reason = (
        message.text.split(None, 1)[1]
        if len(message.text.split()) > 1 and message.reply_to_message
        else "No reason provided."
    )

    if user_id not in BANNED_USERS:
        BANNED_USERS.add(user_id)

    served_chats = [int(chat["chat_id"]) for chat in await get_served_chats()]
    time_expected = get_readable_time(len(served_chats))
    mystic = await message.reply_text(_["gban_5"].format(user_first_name, time_expected))

    number_of_chats = 0
    for chat_id in served_chats:
        try:
            await client.ban_chat_member(chat_id, user_id)
            number_of_chats += 1
            await client.send_message(
                chat_id,
                _["gban_notify"].format(
                    user_first_name,
                    user_id,
                    gban_reason,
                    message.from_user.mention
                )
            )
        except FloodWait as fw:
            await asyncio.sleep(int(fw.value))
        except Exception:
            continue

    db.add_gban(user_id, gban_reason, message.from_user.id)
    await mystic.delete()

@app.on_message(command(["ungban"], sudo_cmd=True))
@language
async def global_un(client, message: Message, localization_dict):
    if len(message.text.split()) == 1:
        await message.reply_text(text=localization_dict["general_1"])
        return
        
    user_id, user_first_name, line  = await extract_user(client, message)
    is_gbanned = db.check_gban(user_id)
    if not is_gbanned:
        return await message.reply_text(localization_dict["gban_7"].format(user_first_name))

    if user_id in BANNED_USERS:
        BANNED_USERS.remove(user_id)

    served_chats = await get_served_chats()
    served_chat_ids = [int(chat["chat_id"]) for chat in served_chats]

    time_expected = get_readable_time(len(served_chat_ids))
    mystic = await message.reply_text(localization_dict["gban_8"].format(user_first_name, time_expected))

    number_of_chats = 0
    for chat_id in served_chat_ids:
        try:
            await client.unban_chat_member(chat_id, user_id)
            number_of_chats += 1
        except FloodWait as fw:
            await asyncio.sleep(int(fw.value))
        except Exception:
            continue

    db.remove_gban(user_id)
    await message.reply_text(localization_dict["gban_9"].format(user_first_name, number_of_chats))
    await mystic.delete()


@app.on_message(command(["gbannedusers", "gbanlist"],sudo_cmd=True))
@language
async def gbanned_list(client, message: Message, _):
    counts = db.count_gbans()
    if counts == 0:
        return await message.reply_text(_["gban_10"])

    mystic = await message.reply_text(_["gban_11"])
    msg = _["gban_12"]

    count = 0
    users = db.list_gbans()  # Use list_gbans() to get all banned users
    for user_data in users:
        count += 1
        user_id = user_data["_id"]
        reason = user_data.get("reason", "No reason provided.")
        banned_by = user_data.get("by", "Unknown")
        ban_time = user_data.get("time", "Unknown")

        try:
            user = await app.get_users(user_id)
            user_mention = user.mention or user.first_name
        except Exception:
            user_mention = str(user_id)

        ban_time_str = ban_time.strftime("%Y-%m-%d %H:%M:%S") if isinstance(ban_time, datetime) else "Unknown"

        msg += (
            f"\n{count}➤ {user_mention}\n"
            f"   • Reason: {reason}\n"
            f"   • Banned By: {banned_by}\n"
            f"   • Date: {ban_time_str}\n"
        )

    if count == 0:
        return await mystic.edit_text(_["gban_10"])
    else:
        return await mystic.edit_text(msg)
