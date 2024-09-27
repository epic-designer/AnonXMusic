import time
from random import choice
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from AnonXMusic.utils.extras import StartPic
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
)
from AnonXMusic.utils.decorators.language import LanguageStart
from AnonXMusic.utils.formatters import get_readable_time
from AnonXMusic.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string
from AnonXMusic.utils.start_utils import get_private_note, get_private_rules
from AnonXMusic.utils.custom_filters import command

@app.on_message(
    command("start") & filters.private & ~BANNED_USERS,
)
@LanguageStart
async def start(c: app, m: Message, _):
    await add_served_user(m.from_user.id)
    # If in a private chat
    if m.chat.type == ChatType.PRIVATE:
        if len(m.text.strip().split()) > 1:
            help_option = m.text.split(None, 1)[1].lower()

            if help_option.startswith("note") and help_option not in ("note", "notes"):
                await get_private_note(c, m, help_option)
                return

            if help_option.startswith("rules"):
                LOGGER(__name__).info(f"{m.from_user.id} fetched privaterules in {m.chat.id}")
                await get_private_rules(c, m, help_option)
                return

            if help_option.startswith("help"):
                help_msg, help_kb = await get_help_msg(m, help_option)
                if help_msg:
                    await m.reply_text(
                        text=help_msg,
                        parse_mode=enums.ParseMode.MARKDOWN,
                        reply_markup=help_kb,
                        quote=True,
                    )
                    return

            if help_option.startswith("sud"):
                await sudoers_list(client=c, message=m, _=_)
                if await is_on_off(2):
                    return await app.send_message(
                        chat_id=Config.LOGGER_ID,
                        text=f"{m.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{m.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{m.from_user.username}",
                    )
                return

            if help_option.startswith("inf"):
                m = await m.reply_text("🔎")
                query = help_option.replace("inf_", "", 1)
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
                    title, duration, views, published, channellink, channel, c.mention
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
                await c.send_photo(
                    chat_id=m.chat.id,
                    photo=thumbnail,
                    caption=searched_text,
                    reply_markup=key,
                )
                if await is_on_off(2):
                    return await c.send_message(
                        chat_id=Config.LOGGER_ID,
                        text=f"{m.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{m.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{m.from_user.username}",
                    )
                return

        # Default start message
        await m.reply_text(
            text=_["start_2"].format(m.from_user.mention, app.mention,str(choice(StartPic))),
            reply_markup=InlineKeyboardMarkup(private_panel(_)),
        )

    # Logging for new users in private chats
    if m.chat.type == ChatType.PRIVATE and await is_on_off(2):
        await c.send_message(
            chat_id=Config.LOGGER_ID,
            text=f"{m.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{m.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{m.from_user.username}",
        )

@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        photo=str(choice(StartPic)),
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)


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

                out = start_panel(_)
                await message.reply_photo(
                    photo=str(choice(StartPic)),
                    caption=_["start_3"].format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)
