import platform
from sys import version as pyver

import psutil
from pyrogram import __version__ as pyrover
from pyrogram import filters
from pyrogram.errors import MessageIdInvalid
from pyrogram.types import InputMediaPhoto, Message
from pytgcalls.__version__ import __version__ as pytgver

import config
from AnonXMusic import app
from AnonXMusic.core.userbot import assistants
from AnonXMusic.misc import SUDOERS, mongodb
from AnonXMusic.plugins import all_plugins
from AnonXMusic.utils.database import get_served_chats, get_served_users, get_sudoers
from AnonXMusic.utils.decorators.language import language, languageCB
from AnonXMusic.utils.inline.stats import back_stats_buttons, stats_buttons
from config import BANNED_USERS
from AnonXMusic.database.antispam_db import GBan
from AnonXMusic.database.approve_db import Approve
from AnonXMusic.database.blacklist_db import Blacklist
from AnonXMusic.database.disable_db import Disabling
from AnonXMusic.database.filters_db import Filters
from AnonXMusic.database.greetings_db import Greetings
from AnonXMusic.database.notes_db import Notes, NotesSettings
from AnonXMusic.database.pins_db import Pins
from AnonXMusic.database.rules_db import Rules
from AnonXMusic.database.warns_db import Warns, WarnSettings
from AnonXMusic.utils.custom_filters import command
from AnonXMusic.database.users_db import Users

@app.on_message(filters.command(["stats", "gstats"]) & filters.group & ~BANNED_USERS)
@language
async def stats_global(client, message: Message, _):
    upl = stats_buttons(_, True if message.from_user.id in SUDOERS else False)
    await message.reply_photo(
        photo=config.STATS_IMG_URL,
        caption=_["gstats_2"].format(app.mention),
        reply_markup=upl,
    )


@app.on_callback_query(filters.regex("stats_back") & ~BANNED_USERS)
@languageCB
async def home_stats(client, CallbackQuery, _):
    upl = stats_buttons(_, True if CallbackQuery.from_user.id in SUDOERS else False)
    await CallbackQuery.edit_message_text(
        text=_["gstats_2"].format(app.mention),
        reply_markup=upl,
    )


@app.on_callback_query(filters.regex("TopOverall") & ~BANNED_USERS)
@languageCB
async def overall_stats(client, CallbackQuery, _):
    await CallbackQuery.answer()
    upl = back_stats_buttons(_)
    try:
        await CallbackQuery.answer()
    except:
        pass
    await CallbackQuery.edit_message_text(_["gstats_1"].format(app.mention))

    # Fetching data asynchronously
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    plugins_list = await all_plugins()  # Await and get the plugins list
    bldb = Blacklist
    gbandb = GBan()
    notesdb = Notes()
    rulesdb = Rules
    grtdb = Greetings
    userdb = Users
    dsbl = Disabling
    appdb = Approve
    fldb = Filters()
    pinsdb = Pins
    notesettings_db = NotesSettings()
    warns_db = Warns
    warns_settings_db = WarnSettings
    
    # Fetch data from each module
    anti_channel_pin = pinsdb.count_chats('antichannelpin')
    clean_linked = pinsdb.count_chats('cleanlinked')
    filters_count = fldb.count_filters_all()
    filters_chats = fldb.count_filters_chats()
    filter_aliases = fldb.count_filter_aliases()
    blacklists_count = bldb.count_blacklists_all()
    blacklists_chats = bldb.count_blackists_chats()
    bl_action_none = bldb.count_action_bl_all('none')
    bl_action_kick = bldb.count_action_bl_all('kick')
    bl_action_warn = bldb.count_action_bl_all('warn')
    bl_action_ban = bldb.count_action_bl_all('ban')
    rules_chats = rulesdb.count_chats_with_rules()
    private_rules = rulesdb.count_privrules_chats()
    warns_total = warns_db.count_warns_total()
    warns_chats = warns_db.count_all_chats_using_warns()
    warned_users = warns_db.count_warned_users()
    warn_kick = warns_settings_db.count_action_chats('kick')
    warn_mute = warns_settings_db.count_action_chats('mute')
    warn_ban = warns_settings_db.count_action_chats('ban')
    notes_total = notesdb.count_all_notes()
    notes_chats = notesdb.count_notes_chats()
    private_notes = notesettings_db.count_chats()
    gbanned_users = gbandb.count_gbans()
    welcome_chats = grtdb.count_chats('welcome')
    approved_total = appdb.count_all_approved()
    approved_chats = appdb.count_approved_chats()
    disabled_items = dsbl.count_disabled_all()
    disabling_chats = dsbl.count_disabling_chats()
    action_del = dsbl.count_action_dis_all('del')
    
    text = _["gstats_3"].format(
        app.mention,
        len(assistants),
        len(BANNED_USERS),
        served_chats,
        served_users,
        len(plugins_list),  # Now we pass the correct length
        len(SUDOERS),
        config.AUTO_LEAVING_ASSISTANT,
        config.DURATION_LIMIT_MIN,
        anti_channel_pin,
        clean_linked,
        filters_count,
        filters_chats,
        filter_aliases,
        blacklists_count,
        blacklists_chats,
        bl_action_none,
        bl_action_kick,
        bl_action_warn,
        bl_action_ban,
        rules_chats,
        private_rules,
        warns_total,
        warns_chats,
        warned_users,
        warn_kick,
        warn_mute,
        warn_ban,
        notes_total,
        notes_chats,
        private_notes,
        gbanned_users,
        welcome_chats,
        approved_total,
        approved_chats,
        disabled_items,
        disabling_chats,
        action_del,        
    )
    med = InputMediaPhoto(media=config.STATS_IMG_URL, caption=text)
    try:
        await CallbackQuery.edit_message_media(media=med, reply_markup=upl)
    except MessageIdInvalid:
        await CallbackQuery.message.reply_photo(
            photo=config.STATS_IMG_URL, caption=text, reply_markup=upl
        )


@app.on_callback_query(filters.regex("bot_stats_sudo"))
@languageCB
async def bot_stats(client, CallbackQuery, _):
    if CallbackQuery.from_user.id not in SUDOERS:
        return await CallbackQuery.answer(_["gstats_4"], show_alert=True)
    upl = back_stats_buttons(_)
    try:
        await CallbackQuery.answer()
    except:
        pass
    await CallbackQuery.edit_message_text(_["gstats_1"].format(app.mention))

    p_core = psutil.cpu_count(logical=False)
    t_core = psutil.cpu_count(logical=True)
    ram = str(round(psutil.virtual_memory().total / (1024.0**3))) + " ɢʙ"
    try:
        cpu_freq = psutil.cpu_freq().current
        if cpu_freq >= 1000:
            cpu_freq = f"{round(cpu_freq / 1000, 2)}ɢʜᴢ"
        else:
            cpu_freq = f"{round(cpu_freq, 2)}ᴍʜᴢ"
    except:
        cpu_freq = "ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ"
    hdd = psutil.disk_usage("/")
    total = hdd.total / (1024.0**3)
    used = hdd.used / (1024.0**3)
    free = hdd.free / (1024.0**3)
    call = await mongodb.command("dbstats")
    datasize = call["dataSize"] / 1024
    storage = call["storageSize"] / 1024
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    plugins_list = await all_plugins()  # Await and get the plugins list

    text = _["gstats_5"].format(
        app.mention,
        len(plugins_list),  # Now we pass the correct length
        platform.system(),
        ram,
        p_core,
        t_core,
        cpu_freq,
        pyver.split()[0],
        pyrover,
        pytgver,
        str(total)[:4],
        str(used)[:4],
        str(free)[:4],
        served_chats,
        served_users,
        len(BANNED_USERS),
        len(await get_sudoers()),
        str(datasize)[:6],
        storage,
        call["collections"],
        call["objects"],
    )
    med = InputMediaPhoto(media=config.STATS_IMG_URL, caption=text)
    try:
        await CallbackQuery.edit_message_media(media=med, reply_markup=upl)
    except MessageIdInvalid:
        await CallbackQuery.message.reply_photo(
            photo=config.STATS_IMG_URL, caption=text, reply_markup=upl
        )
