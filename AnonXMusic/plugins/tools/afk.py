
import time
import re

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from AnonXMusic.utils.database import add_afk, cleanmode_off, cleanmode_on, is_afk, remove_afk
from AnonXMusic import app
from AnonXMusic.core.decorator.permissions import adminsOnly
from AnonXMusic.utils import get_readable_time as get_readable_time2
from utils import put_cleanmode

__PLUGIN__ = "AFK"
__HELP__ = """/afk [Reason > Optional] - Tell others that you are AFK (Away From Keyboard), so that your boyfriend or girlfriend won't look for you.
/afk [reply to media] - AFK with media.
/afkdel - Enable auto delete AFK message in group (Only for group admin). Default is **Enable**.
Just type something in group to remove AFK Status."""


# Handle set AFK Command
@app.on_cmd("afk")
async def active_afk(_, ctx: Message):
    if ctx.sender_chat:
        return await ctx.reply_msg("You cannot use this command in a channel.", del_in=6)
    user_id = ctx.from_user.id
    verifier, reasondb = await is_afk(user_id)
    if verifier:
        await remove_afk(user_id)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            data = reasondb["data"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time2((int(time.time() - timeafk)))
            if afktype == "animation":
                send = (
                    await ctx.reply_animation(
                        data,
                        caption=f"Welcome back, {ctx.from_user.mention}! You were AFK for {seenago}.",
                    )
                    if str(reasonafk) == "None"
                    else await ctx.reply_animation(
                        data,
                        caption=f"Welcome back, {ctx.from_user.mention}! You were AFK for {seenago}. Reason: {reasonafk}",
                    )
                )
            elif afktype == "photo":
                send = (
                    await ctx.reply_photo(
                        photo=f"downloads/{user_id}.jpg",
                        caption=f"Welcome back, {ctx.from_user.mention}! You were AFK for {seenago}.",
                    )
                    if str(reasonafk) == "None"
                    else await ctx.reply_photo(
                        photo=f"downloads/{user_id}.jpg",
                        caption=f"Welcome back, {ctx.from_user.mention}! You were AFK for {seenago}. Reason: {reasonafk}",
                    )
                )
            elif afktype == "text":
                send = await ctx.reply_text(
                    f"Welcome back, {ctx.from_user.mention}! You were AFK for {seenago}.",
                    disable_web_page_preview=True,
                )
            elif afktype == "text_reason":
                send = await ctx.reply_text(
                    f"Welcome back, {ctx.from_user.mention}! You were AFK for {seenago}. Reason: {reasonafk}",
                    disable_web_page_preview=True,
                )
        except Exception:
            send = await ctx.reply_text(
                f"{ctx.from_user.first_name} is now online.",
                disable_web_page_preview=True,
            )
        await put_cleanmode(ctx.chat.id, send.id)
        return

    if len(ctx.command) == 1 and not ctx.reply_to_message:
        details = {
            "type": "text",
            "time": time.time(),
            "data": None,
            "reason": None,
        }
    elif len(ctx.command) > 1 and not ctx.reply_to_message:
        _reason = (ctx.text.split(None, 1)[1].strip())[:100]
        details = {
            "type": "text_reason",
            "time": time.time(),
            "data": None,
            "reason": _reason,
        }
    elif len(ctx.command) == 1 and ctx.reply_to_message.animation:
        _data = ctx.reply_to_message.animation.file_id
        details = {
            "type": "animation",
            "time": time.time(),
            "data": _data,
            "reason": None,
        }
    elif len(ctx.command) > 1 and ctx.reply_to_message.animation:
        _data = ctx.reply_to_message.animation.file_id
        _reason = (ctx.text.split(None, 1)[1].strip())[:100]
        details = {
            "type": "animation",
            "time": time.time(),
            "data": _data,
            "reason": _reason,
        }
    elif len(ctx.command) == 1 and ctx.reply_to_message.photo:
        await app.download_media(ctx.reply_to_message, file_name=f"{user_id}.jpg")
        details = {
            "type": "photo",
            "time": time.time(),
            "data": None,
            "reason": None,
        }
    elif len(ctx.command) > 1 and ctx.reply_to_message.photo:
        await app.download_media(ctx.reply_to_message, file_name=f"{user_id}.jpg")
        _reason = ctx.text.split(None, 1)[1].strip()
        details = {
            "type": "photo",
            "time": time.time(),
            "data": None,
            "reason": _reason,
        }
    elif len(ctx.command) == 1 and ctx.reply_to_message.sticker:
        if ctx.reply_to_message.sticker.is_animated:
            details = {
                "type": "text",
                "time": time.time(),
                "data": None,
                "reason": None,
            }
        else:
            await app.download_media(ctx.reply_to_message, file_name=f"{user_id}.jpg")
            details = {
                "type": "photo",
                "time": time.time(),
                "data": None,
                "reason": None,
            }
    elif len(ctx.command) > 1 and ctx.reply_to_message.sticker:
        _reason = (ctx.text.split(None, 1)[1].strip())[:100]
        if ctx.reply_to_message.sticker.is_animated:
            details = {
                "type": "text_reason",
                "time": time.time(),
                "data": None,
                "reason": _reason,
            }
        else:
            await app.download_media(ctx.reply_to_message, file_name=f"{user_id}.jpg")
            details = {
                "type": "photo",
                "time": time.time(),
                "data": None,
                "reason": _reason,
            }
    else:
        details = {
            "type": "text",
            "time": time.time(),
            "data": None,
            "reason": None,
        }

    await add_afk(user_id, details)
    send = await ctx.reply_msg(
        f"{ctx.from_user.mention} is now AFK.",
    )
    await put_cleanmode(ctx.chat.id, send.id)


@app.on_cmd("afkdel", group_only=True)
@adminsOnly("can_change_info")
async def afk_state(_, ctx: Message):
    if not ctx.from_user:
        return
    if len(ctx.command) == 1:
        return await ctx.reply_msg(
            f"Usage: /{ctx.command[0]} [enable/disable]", del_in=6
        )
    chat_id = ctx.chat.id
    state = ctx.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        await cleanmode_on(chat_id)
        await ctx.reply_msg("AFK auto-delete enabled.")
    elif state == "disable":
        await cleanmode_off(chat_id)
        await ctx.reply_msg("AFK auto-delete disabled.")
    else:
        await ctx.reply_msg(f"Usage: /{ctx.command[0]} [enable/disable]", del_in=6)


@app.on_message(
    filters.group & ~filters.bot & ~filters.via_bot,
    group=1,
)
async def afk_watcher_func(self: Client, ctx: Message):
    if ctx.sender_chat:
        return
    userid = ctx.from_user.id
    user_name = ctx.from_user.mention
    if ctx.entities:
        possible = ["/afk", f"/afk@{self.me.username}", "!afk"]
        message_text = ctx.text or ctx.caption
        for entity in ctx.entities:
            try:
                if (
                    entity.type == enums.MessageEntityType.BOT_COMMAND
                    and (message_text[0 : 0 + entity.length]).lower() in possible
                ):
                    return
            except UnicodeDecodeError:
                return

    msg = ""
    replied_user_id = 0

    # Self AFK
    verifier, reasondb = await is_afk(userid)
    if verifier:
        await remove_afk(userid)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            data = reasondb["data"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time2((int(time.time() - timeafk)))
            if afktype == "text":
                msg += f"{user_name} is back online after being AFK for {seenago}."
            if afktype == "text_reason":
                msg += f"{user_name} is back online after being AFK for {seenago}. Reason: {reasonafk}"
            if afktype == "animation":
                send = (
                    await ctx.reply_animation(
                        data,
                        caption=f"{user_name} is back online after being AFK for {seenago}.",
                    )
                    if str(reasonafk) == "None"
                    else await ctx.reply_animation(
                        data,
                        caption=f"{user_name} is back online after being AFK for {seenago}. Reason: {reasonafk}",
                    )
                )
            elif afktype == "photo":
                send = (
                    await ctx.reply_photo(
                        photo=f"downloads/{userid}.jpg",
                        caption=f"{user_name} is back online after being AFK for {seenago}.",
                    )
                    if str(reasonafk) == "None"
                    else await ctx.reply_photo(
                        photo=f"downloads/{userid}.jpg",
                        caption=f"{user_name} is back online after being AFK for {seenago}. Reason: {reasonafk}",
                    )
                )
            await put_cleanmode(ctx.chat.id, send.id)
        except Exception:
            await ctx.reply_text(
                f"{user_name} is back online after being AFK for {seenago}."
            )

    # Handle AFK Replies
    if ctx.reply_to_message:
        if ctx.reply_to_message.from_user:
            replied_user_id = ctx.reply_to_message.from_user.id
            if replied_user_id == userid:
                return

    elif ctx.entities:
        for entity in ctx.entities:
            if entity.type == enums.MessageEntityType.TEXT_MENTION:
                replied_user_id = entity.user.id
            if entity.type == enums.MessageEntityType.MENTION:
                replied_user = await self.get_users(ctx.text[entity.offset : entity.offset + entity.length])
                replied_user_id = replied_user.id

    if replied_user_id:
        verifier, reasondb = await is_afk(replied_user_id)
        if verifier:
            reasonafk = reasondb["reason"]
            if str(reasonafk) == "None":
                reasonafk = ""
            else:
                reasonafk = f"\nReason: {reasonafk}"

            timeafk = reasondb["time"]
            seenago = get_readable_time2((int(time.time() - timeafk)))
            await ctx.reply_text(
                f"{ctx.reply_to_message.from_user.first_name} is currently AFK (away from keyboard).\n"
                f"AFK for: {seenago}{reasonafk}"
            )
            