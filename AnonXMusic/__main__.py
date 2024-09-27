import asyncio
import importlib
from pyrogram import idle, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message, InputMediaPhoto
from pyrogram.errors import MessageNotModified
import sys
import os
from threading import RLock
import config
from AnonXMusic import LOGGER, app, userbot, load_cmds, scheduler
from AnonXMusic.misc import sudo
from AnonXMusic.plugins import all_plugins  # Import the all_plugins function
from AnonXMusic.supports import *
from AnonXMusic.database import MongoDB
from AnonXMusic.utils.database import get_banned_users, get_gbanned
from AnonXMusic.core.call import Anony
from config import BANNED_USERS
from strings import get_string

INITIAL_LOCK = RLock()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

async def init():
    if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER(__name__).warning(f"Error loading banned users: {e}")
    
    await app.start()

    # Get cmds and keys
    cmd_list = await load_cmds(await all_plugins())  # Load the plugins here
    await load_support_users()
    LOGGER("AnonXMusic.plugins").info(f"Plugins Loaded: {cmd_list}")
    
    await userbot.start()
    await Anony.start()
    await Anony.decorators()
    
    LOGGER("AnonXMusic").info("AnonX Music Bot Started Successfully.")
    await idle()
    await app.stop()
    await userbot.stop()
    
    MongoDB.close()
    LOGGER("AnonXMusic").info("Stopping AnonX Music Bot...")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
