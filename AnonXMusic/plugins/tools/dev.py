import os
import re
import subprocess
import subprocess as subp
import sys
import traceback
from traceback import format_exc
from asyncio import create_subprocess_shell, sleep, subprocess
from inspect import getfullargspec
from io import StringIO,BytesIO
from os import execvp
from sys import executable
from time import time

from pyrogram import filters
from pyrogram.errors import (ChannelInvalid, ChannelPrivate, ChatAdminRequired,
                             EntityBoundsInvalid, FloodWait, MessageTooLong,
                             PeerIdInvalid, RPCError)
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM
from pyrogram.types import Message

from AnonXMusic import app, LOGGER

from AnonXMusic.database import MongoDB
from AnonXMusic.database.chats_db import Chats
from AnonXMusic.database.support_db import SUPPORTS
from AnonXMusic.database.users_db import Users
from AnonXMusic.plugins.tools.scheduled_jobs import clean_my_db
from AnonXMusic.supports import get_support_staff
from AnonXMusic.utils.clean_file import remove_markdown_and_html
from AnonXMusic.utils.custom_filters import command
from AnonXMusic.utils.extract_user import extract_user
from AnonXMusic.utils.parser import mention_markdown

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import OWNER_ID
import config as Config

def can_change_type(curr, to_user):
    if curr == "dev" and to_user in ["whitelist","sudo"]:
        return True
    elif curr == "sudo" and to_user == "whitelist":
        return True
    else:
        return False

@app.on_message(command(["addsupport"]))
async def add_support(c: app, m:Message):
    support = SUPPORTS()
    curr_user = support.get_support_type(m.from_user.id)
    if not curr_user:
        await m.reply_text("Stay in you limit")
        return
    split = m.command
    reply_to = m.reply_to_message
    if reply_to:
        try:
            userr = reply_to.from_user.id
        except Exception:
            await m.reply_text("Reply to an user")
            return
        curr = support.get_support_type(userr)
        try:
            to = split[1].lower()
        except IndexError:
            await m.reply_text("**USAGE**\n/addsupport [reply to message | user id] [dev | sudo | whitelist]")
            return
        if to not in ["dev","sudo","whitelist"]:
            await m.reply_text("**USAGE**\n/addsupport [reply to message | user id] [dev | sudo | whitelist]")
            return
        if m.from_user.id == int(OWNER_ID):
            if to == curr:
                await m.reply_text(f"This user is already in {to} users")
                return
            elif curr:
                kb = IKM(
                    [
                        [
                            IKB("Yes",f"change_support_type:{to}"),
                            IKB("No","change_support_type:no")
                        ]
                    ]
                )
                await m.reply_text(f"This is user is already in {curr} users\nDo you want to make him {to} user?",reply_markup=kb)
                return
            else:
                support.insert_support_user(userr,to)
                await m.reply_text(f"This user is now a {to} user")
                return
        can_do = can_change_type(curr_user,to)
        if can_do:
            if to == curr:
                await m.reply_text(f"This user is already in {to} users")
                return
            elif curr:
                kb = IKM(
                    [
                        [
                            IKB("Yes",f"change_support_type:{to}"),
                            IKB("No","change_support_type:no")
                        ]
                    ]
                )
                await m.reply_text(f"This is user is already in {curr} users\nDo you want to make him {to} user?",reply_markup=kb)
                return
            else:
                support.insert_support_user(userr,to)
                await m.reply_text(f"This user is now a {to} user")
                return
        else:
            await m.reply_text("Sorry you can't do it")
            return
    elif len(split) >= 3:
        user = split[1]
        try:
            userr,_,_ = extract_user(user)
        except Exception:
            await m.reply_text("Tell the user to start me first")
            return
        curr = support.get_support_type(userr)
        try:
            to = m.command[2].lower()
        except IndexError:
            await m.reply_text("**USAGE**\n/addsupport [reply to message | user id | username] [dev | sudo | whitelist]")
            return
        if to not in ["dev","sudo","whitelist"]:
            await m.reply_text("**USAGE**\n/addsupport [reply to message | user id] [dev | sudo | whitelist]")
            return
        if m.from_user.id == int(OWNER_ID):
            if to == curr:
                await m.reply_text(f"This user is already in {to} users")
                return
            elif curr:
                kb = IKM(
                    [
                        [
                            IKB("Yes",f"change_support_type:{to}"),
                            IKB("No","change_support_type:no")
                        ]
                    ]
                )
                await m.reply_text(f"This is user is already in {curr} users\nDo you want to make him {to} user?",reply_markup=kb)
                return
            else:
                support.insert_support_user(userr,to)
                await m.reply_text(f"This user is now a {to} user")
                return
        can_do = can_change_type(curr_user,to)
        if can_do:
            if to == curr:
                await m.reply_text(f"This user is already in {to} users")
                return
            elif curr:
                kb = IKM(
                    [
                        [
                            IKB("Yes",f"change_support_type:{to}"),
                            IKB("No","change_support_type:no")
                        ]
                    ]
                )
                await m.reply_text(f"This is user is already in {curr} users\nDo you want to make him {to} user?",reply_markup=kb)
                return
            else:
                support.insert_support_user(userr,to)
                await m.reply_text(f"This user is now a {to} user")
                return
        else:
            await m.reply_text("Sorry you can't do it")
            return

@app.on_message(command("rmsupport"))
async def rm_support(c: app, m: Message):
    support = SUPPORTS()
    curr_user = support.get_support_type(m.from_user.id)
    if not curr_user:
        await m.reply_text("Stay in you limit")
        return
    split = m.command
    reply_to = m.reply_to_message

    if reply_to:
        try:
            curr = reply_to.from_user.id
        except Exception:
            await m.reply_text("Reply to an user")
            return
    elif len(split) >= 2:
        try:
            curr,_,_ = extract_user(m)
        except Exception:
            await m.reply_text("Dunno who u r talking abt")
            return
    else:
        await m.reply_text("**USAGE**\n/rmsupport [reply to user | user id | username]")
        return
    to_user = support.get_support_type(curr)
    can_user = can_change_type(curr_user,to_user)
    if m.from_user.id == int(OWNER_ID) or can_user:
        support.delete_support_user(curr)
        await m.reply_text("Done! User now no longer belongs to the support staff")
    else:
        await m.reply_text("Sorry you can't do that...")
    return



@app.on_message(command("chatlist", dev_cmd=True))
async def chats(c: app, m: Message):
    exmsg = await m.reply_text(text="Exporting Charlist...")
    await c.send_message(
        Config.LOGGER_ID,
        f"#CHATLIST\n\n**User:** {(await mention_markdown(m.from_user.first_name, m.from_user.id))}",
    )
    all_chats = (Chats.list_chats_full()) or {}
    chatfile = """List of chats in my database.

        <b>Chat name | Chat ID | Members count</b>"""
    P = 1
    for chat in all_chats:
        try:
            chat_info = await c.get_chat(chat["_id"])
            chat_members = chat_info.members_count
            try:
                invitelink = chat_info.invite_link
            except KeyError:
                invitelink = "No Link!"
            chatfile += f"{P}. {chat['chat_name']} | {chat['_id']} | {chat_members} | {invitelink}\n"
            P += 1
        except ChatAdminRequired:
            pass
        except (ChannelPrivate, ChannelInvalid):
            Chats.remove_chat(chat["_id"])
        except PeerIdInvalid:
            LOGGER(__name__).warning(f"Peer not found {chat['_id']}")
        except FloodWait as ef:
            LOGGER(__name__).error("FloodWait required, Sleeping for 60s")
            LOGGER(__name__).error(ef)
            sleep(60)
        except RPCError as ef:
            LOGGER(__name__).error(ef)
            await m.reply_text(f"**Error:**\n{ef}")

    with BytesIO(str.encode(await remove_markdown_and_html(chatfile))) as f:
        f.name = "chatlist.txt"
        await m.reply_document(
            document=f,
            caption="Here is the list of chats in my Database.",
        )
    await exmsg.delete()
    return


@app.on_message(command("leavechat", dev_cmd=True))
async def leave_chat(c: app, m: Message):
    if len(m.text.split()) != 2:
        await m.reply_text("Supply a chat id which I should leave!", quoet=True)
        return

    chat_id = m.text.split(None, 1)[1]

    replymsg = await m.reply_text(f"Trying to leave chat {chat_id}...", quote=True)
    try:
        await c.leave_chat(chat_id)
        await replymsg.edit_text(f"Left <code>{chat_id}</code>.")
    except PeerIdInvalid:
        await replymsg.edit_text("Haven't seen this group in this session!")
    except RPCError as ef:
        LOGGER(__name__).error(ef)
        await replymsg.edit_text(f"Failed to leave chat!\nError: <code>{ef}</code>.")
    return


@app.on_message(command(["cleandb","cleandatabase"],sudo_cmd=True))
async def cleeeen(c:app,m:Message):
    x = await m.reply_text("Cleaning the database...")
    try:
        z = await clean_my_db(c,True,m.from_user.id)
        try:
            await x.delete()
        except Exception:
            pass
        await m.reply_text(z)
        return
    except Exception as e:
        await m.reply_text(e)
        await x.delete()
        LOGGER(__name__).error(e)
        LOGGER(__name__).error(format_exc())
        return

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})


@app.on_edited_message(
    filters.command("eval")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot
)
@app.on_message(
    filters.command("eval")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot
)
async def executor(client: app, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="<b>ᴡʜᴀᴛ ʏᴏᴜ ᴡᴀɴɴᴀ ᴇxᴇᴄᴜᴛᴇ ʙᴀʙʏ ?</b>")
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.delete()
    t1 = time()
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = "\n"
    if exc:
        evaluation += exc
    elif stderr:
        evaluation += stderr
    elif stdout:
        evaluation += stdout
    else:
        evaluation += "Success"
    final_output = f"<b>⥤ ʀᴇsᴜʟᴛ :</b>\n<pre language='python'>{evaluation}</pre>"
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation))
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⏳",
                        callback_data=f"runtime {t2-t1} Seconds",
                    )
                ]
            ]
        )
        await message.reply_document(
            document=filename,
            caption=f"<b>⥤ ᴇᴠᴀʟ :</b>\n<code>{cmd[0:980]}</code>\n\n<b>⥤ ʀᴇsᴜʟᴛ :</b>\nAttached Document",
            quote=False,
            reply_markup=keyboard,
        )
        await message.delete()
        os.remove(filename)
    else:
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⏳",
                        callback_data=f"runtime {round(t2-t1, 3)} Seconds",
                    ),
                    InlineKeyboardButton(
                        text="🗑",
                        callback_data=f"forceclose abc|{message.from_user.id}",
                    ),
                ]
            ]
        )
        await edit_or_reply(message, text=final_output, reply_markup=keyboard)


@app.on_callback_query(filters.regex(r"runtime"))
async def runtime_func_cq(_, cq):
    runtime = cq.data.split(None, 1)[1]
    await cq.answer(runtime, show_alert=True)


@app.on_callback_query(filters.regex("forceclose"))
async def forceclose_command(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    query, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer(
                "» ɪᴛ'ʟʟ ʙᴇ ʙᴇᴛᴛᴇʀ ɪғ ʏᴏᴜ sᴛᴀʏ ɪɴ ʏᴏᴜʀ ʟɪᴍɪᴛs ʙᴀʙʏ.", show_alert=True
            )
        except:
            return
    await CallbackQuery.message.delete()
    try:
        await CallbackQuery.answer()
    except:
        return


@app.on_edited_message(
    filters.command("sh")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot
)
@app.on_message(
    filters.command("sh")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot
)
async def shellrunner(_, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="<b>ᴇxᴀᴍᴩʟᴇ :</b>\n/sh git pull")
    text = message.text.split(None, 1)[1]
    if "\n" in text:
        code = text.split("\n")
        output = ""
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            except Exception as err:
                await edit_or_reply(message, text=f"<b>ERROR :</b>\n<pre>{err}</pre>")
            output += f"<b>{code}</b>\n"
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", text)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as err:
            print(err)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type,
                value=exc_obj,
                tb=exc_tb,
            )
            return await edit_or_reply(
                message, text=f"<b>ERROR :</b>\n<pre>{''.join(errors)}</pre>"
            )
        output = process.stdout.read()[:-1].decode("utf-8")
    if str(output) == "\n":
        output = None
    if output:
        if len(output) > 4096:
            with open("output.txt", "w+") as file:
                file.write(output)
            await app.send_document(
                message.chat.id,
                "output.txt",
                reply_to_message_id=message.id,
                caption="<code>Output</code>",
            )
            return os.remove("output.txt")
        await edit_or_reply(message, text=f"<b>OUTPUT :</b>\n<pre>{output}</pre>")
    else:
        await edit_or_reply(message, text="<b>OUTPUT :</b>\n<code>None</code>")
    await message.stop_propagation()

__PLUGIN__ = "devs"


__HELP__ = """
**DEV and SUDOERS commands**

**Owner's commands:**
• /restart : Restart the bot
• /update : To update the bot with the main stream repo

**Dev's commands:**
• /addsupport [dev | sudo | whitelist] : Reply to message or give me user id or username
• /logs : Return the logs of bot.
• /eval : Evaluate the given python code.
• /chatlist : Return the list of chats present in database
• /leavechat : Bot will leave the provided chat.
• /broadcast : Broadcast the messge to chats.
    Available tags:
     `-u` : For users
     `-c` : For chats
     `-all` : For all

**Sudoer's command:**
• /ping : return the ping of the bot.
• /cleandb : Delete useless junks from database (Automatically start cleaning it at 3:00:00 AM)

**Example:**
/ping
"""
