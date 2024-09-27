import random
from typing import Dict, List, Union ,Iterable
from pyrogram.enums import ChatType
import pytz
from datetime import datetime
from config import OWNER_ID
from AnonXMusic import userbot
from AnonXMusic.core.mongo import mongodb



authdb = mongodb.adminauth
authuserdb = mongodb.authuser
autoenddb = mongodb.autoend
assdb = mongodb.assistants
blacklist_chatdb = mongodb.blacklistChat
blockeddb = mongodb.blockedusers
chatsdb = mongodb.chats
channeldb = mongodb.cplaymode
countdb = mongodb.upcount
gbansdb = mongodb.gban
langdb = mongodb.language
onoffdb = mongodb.onoffper
playmodedb = mongodb.playmode
playtypedb = mongodb.playtypedb
skipdb = mongodb.skipmode
sudoersdb = mongodb.sudoers
usersdb = mongodb.tgusersdb
cleandb = mongodb.tgcleandb
localesdb = mongodb.localesdb
afkdb = mongodb.afk
coupledb = mongodb.couple
filtersdb = mongodb.filters
warnsdb = mongodb.warns
approve_col = mongodb.approvedb
welcome_col = mongodb.welcomedb
locks_col = mongodb.locksdb
fedsdb = mongodb.fedsdbb

# Shifting to memory [mongo sucks often]
active = []
activevideo = []
assistantdict = {}
autoend = {}
count = {}
channelconnect = {}
langm = {}
loop = {}
maintenance = []
nonadmin = {}
pause = {}
playmode = {}
playtype = {}
skipmode = {}
cleanmode = {}



async def get_assistant_number(chat_id: int) -> str:
    assistant = assistantdict.get(chat_id)
    return assistant




async def get_client(assistant: int):
    if int(assistant) == 1:
        return userbot.one
    elif int(assistant) == 2:
        return userbot.two
    elif int(assistant) == 3:
        return userbot.three
    elif int(assistant) == 4:
        return userbot.four
    elif int(assistant) == 5:
        return userbot.five




async def set_assistant_new(chat_id, number):
    number = int(number)
    await assdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": number}},
        upsert=True,
    )




async def set_assistant(chat_id):
    from AnonXMusic.core.userbot import assistants


    ran_assistant = random.choice(assistants)
    assistantdict[chat_id] = ran_assistant
    await assdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": ran_assistant}},
        upsert=True,
    )
    userbot = await get_client(ran_assistant)
    return userbot




async def get_assistant(chat_id: int) -> str:
    from AnonXMusic.core.userbot import assistants


    assistant = assistantdict.get(chat_id)
    if not assistant:
        dbassistant = await assdb.find_one({"chat_id": chat_id})
        if not dbassistant:
            userbot = await set_assistant(chat_id)
            return userbot
        else:
            got_assis = dbassistant["assistant"]
            if got_assis in assistants:
                assistantdict[chat_id] = got_assis
                userbot = await get_client(got_assis)
                return userbot
            else:
                userbot = await set_assistant(chat_id)
                return userbot
    else:
        if assistant in assistants:
            userbot = await get_client(assistant)
            return userbot
        else:
            userbot = await set_assistant(chat_id)
            return userbot




async def set_calls_assistant(chat_id):
    from AnonXMusic.core.userbot import assistants


    ran_assistant = random.choice(assistants)
    assistantdict[chat_id] = ran_assistant
    await assdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": ran_assistant}},
        upsert=True,
    )
    return ran_assistant




async def group_assistant(self, chat_id: int) -> int:
    from AnonXMusic.core.userbot import assistants


    assistant = assistantdict.get(chat_id)
    if not assistant:
        dbassistant = await assdb.find_one({"chat_id": chat_id})
        if not dbassistant:
            assis = await set_calls_assistant(chat_id)
        else:
            assis = dbassistant["assistant"]
            if assis in assistants:
                assistantdict[chat_id] = assis
                assis = assis
            else:
                assis = await set_calls_assistant(chat_id)
    else:
        if assistant in assistants:
            assis = assistant
        else:
            assis = await set_calls_assistant(chat_id)
    if int(assis) == 1:
        return self.one
    elif int(assis) == 2:
        return self.two
    elif int(assis) == 3:
        return self.three
    elif int(assis) == 4:
        return self.four
    elif int(assis) == 5:
        return self.five




async def is_skipmode(chat_id: int) -> bool:
    mode = skipmode.get(chat_id)
    if not mode:
        user = await skipdb.find_one({"chat_id": chat_id})
        if not user:
            skipmode[chat_id] = True
            return True
        skipmode[chat_id] = False
        return False
    return mode




async def skip_on(chat_id: int):
    skipmode[chat_id] = True
    user = await skipdb.find_one({"chat_id": chat_id})
    if user:
        return await skipdb.delete_one({"chat_id": chat_id})




async def skip_off(chat_id: int):
    skipmode[chat_id] = False
    user = await skipdb.find_one({"chat_id": chat_id})
    if not user:
        return await skipdb.insert_one({"chat_id": chat_id})




async def get_upvote_count(chat_id: int) -> int:
    mode = count.get(chat_id)
    if not mode:
        mode = await countdb.find_one({"chat_id": chat_id})
        if not mode:
            return 5
        count[chat_id] = mode["mode"]
        return mode["mode"]
    return mode




async def set_upvotes(chat_id: int, mode: int):
    count[chat_id] = mode
    await countdb.update_one(
        {"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True
    )




async def is_autoend() -> bool:
    chat_id = 1234
    user = await autoenddb.find_one({"chat_id": chat_id})
    if not user:
        return False
    return True




async def autoend_on():
    chat_id = 1234
    await autoenddb.insert_one({"chat_id": chat_id})




async def autoend_off():
    chat_id = 1234
    await autoenddb.delete_one({"chat_id": chat_id})




async def get_loop(chat_id: int) -> int:
    lop = loop.get(chat_id)
    if not lop:
        return 0
    return lop




async def set_loop(chat_id: int, mode: int):
    loop[chat_id] = mode




async def get_cmode(chat_id: int) -> int:
    mode = channelconnect.get(chat_id)
    if not mode:
        mode = await channeldb.find_one({"chat_id": chat_id})
        if not mode:
            return None
        channelconnect[chat_id] = mode["mode"]
        return mode["mode"]
    return mode




async def set_cmode(chat_id: int, mode: int):
    channelconnect[chat_id] = mode
    await channeldb.update_one(
        {"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True
    )




async def get_playtype(chat_id: int) -> str:
    mode = playtype.get(chat_id)
    if not mode:
        mode = await playtypedb.find_one({"chat_id": chat_id})
        if not mode:
            playtype[chat_id] = "Everyone"
            return "Everyone"
        playtype[chat_id] = mode["mode"]
        return mode["mode"]
    return mode




async def set_playtype(chat_id: int, mode: str):
    playtype[chat_id] = mode
    await playtypedb.update_one(
        {"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True
    )




async def get_playmode(chat_id: int) -> str:
    mode = playmode.get(chat_id)
    if not mode:
        mode = await playmodedb.find_one({"chat_id": chat_id})
        if not mode:
            playmode[chat_id] = "Direct"
            return "Direct"
        playmode[chat_id] = mode["mode"]
        return mode["mode"]
    return mode




async def set_playmode(chat_id: int, mode: str):
    playmode[chat_id] = mode
    await playmodedb.update_one(
        {"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True
    )




async def get_lang(chat_id: int) -> str:
    mode = langm.get(chat_id)
    if not mode:
        lang = await langdb.find_one({"chat_id": chat_id})
        if not lang:
            langm[chat_id] = "en"
            return "en"
        langm[chat_id] = lang["lang"]
        return lang["lang"]
    return mode




async def set_lang(chat_id: int, lang: str):
    langm[chat_id] = lang
    await langdb.update_one({"chat_id": chat_id}, {"$set": {"lang": lang}}, upsert=True)




async def is_music_playing(chat_id: int) -> bool:
    mode = pause.get(chat_id)
    if not mode:
        return False
    return mode




async def music_on(chat_id: int):
    pause[chat_id] = True




async def music_off(chat_id: int):
    pause[chat_id] = False




async def get_active_chats() -> list:
    return active




async def is_active_chat(chat_id: int) -> bool:
    if chat_id not in active:
        return False
    else:
        return True




async def add_active_chat(chat_id: int):
    if chat_id not in active:
        active.append(chat_id)




async def remove_active_chat(chat_id: int):
    if chat_id in active:
        active.remove(chat_id)




async def get_active_video_chats() -> list:
    return activevideo




async def is_active_video_chat(chat_id: int) -> bool:
    if chat_id not in activevideo:
        return False
    else:
        return True




async def add_active_video_chat(chat_id: int):
    if chat_id not in activevideo:
        activevideo.append(chat_id)




async def remove_active_video_chat(chat_id: int):
    if chat_id in activevideo:
        activevideo.remove(chat_id)




async def check_nonadmin_chat(chat_id: int) -> bool:
    user = await authdb.find_one({"chat_id": chat_id})
    if not user:
        return False
    return True




async def is_nonadmin_chat(chat_id: int) -> bool:
    mode = nonadmin.get(chat_id)
    if not mode:
        user = await authdb.find_one({"chat_id": chat_id})
        if not user:
            nonadmin[chat_id] = False
            return False
        nonadmin[chat_id] = True
        return True
    return mode




async def add_nonadmin_chat(chat_id: int):
    nonadmin[chat_id] = True
    is_admin = await check_nonadmin_chat(chat_id)
    if is_admin:
        return
    return await authdb.insert_one({"chat_id": chat_id})




async def remove_nonadmin_chat(chat_id: int):
    nonadmin[chat_id] = False
    is_admin = await check_nonadmin_chat(chat_id)
    if not is_admin:
        return
    return await authdb.delete_one({"chat_id": chat_id})




async def is_on_off(on_off: int) -> bool:
    onoff = await onoffdb.find_one({"on_off": on_off})
    if not onoff:
        return False
    return True




async def add_on(on_off: int):
    is_on = await is_on_off(on_off)
    if is_on:
        return
    return await onoffdb.insert_one({"on_off": on_off})




async def add_off(on_off: int):
    is_off = await is_on_off(on_off)
    if not is_off:
        return
    return await onoffdb.delete_one({"on_off": on_off})




async def is_maintenance():
    if not maintenance:
        get = await onoffdb.find_one({"on_off": 1})
        if not get:
            maintenance.clear()
            maintenance.append(2)
            return True
        else:
            maintenance.clear()
            maintenance.append(1)
            return False
    else:
        if 1 in maintenance:
            return False
        else:
            return True




async def maintenance_off():
    maintenance.clear()
    maintenance.append(2)
    is_off = await is_on_off(1)
    if not is_off:
        return
    return await onoffdb.delete_one({"on_off": 1})




async def maintenance_on():
    maintenance.clear()
    maintenance.append(1)
    is_on = await is_on_off(1)
    if is_on:
        return
    return await onoffdb.insert_one({"on_off": 1})




async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True




async def get_served_users() -> list:
    users_list = []
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list




async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": user_id})




async def get_served_chats() -> list:
    chats_list = []
    async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list




async def is_served_chat(chat_id: int) -> bool:
    chat = await chatsdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True




async def add_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if is_served:
        return
    return await chatsdb.insert_one({"chat_id": chat_id})




async def blacklisted_chats() -> list:
    chats_list = []
    async for chat in blacklist_chatdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat["chat_id"])
    return chats_list




async def blacklist_chat(chat_id: int) -> bool:
    if not await blacklist_chatdb.find_one({"chat_id": chat_id}):
        await blacklist_chatdb.insert_one({"chat_id": chat_id})
        return True
    return False




async def whitelist_chat(chat_id: int) -> bool:
    if await blacklist_chatdb.find_one({"chat_id": chat_id}):
        await blacklist_chatdb.delete_one({"chat_id": chat_id})
        return True
    return False




async def _get_authusers(chat_id: int) -> Dict[str, int]:
    _notes = await authuserdb.find_one({"chat_id": chat_id})
    if not _notes:
        return {}
    return _notes["notes"]




async def get_authuser_names(chat_id: int) -> List[str]:
    _notes = []
    for note in await _get_authusers(chat_id):
        _notes.append(note)
    return _notes




async def get_authuser(chat_id: int, name: str) -> Union[bool, dict]:
    name = name
    _notes = await _get_authusers(chat_id)
    if name in _notes:
        return _notes[name]
    else:
        return False




async def save_authuser(chat_id: int, name: str, note: dict):
    name = name
    _notes = await _get_authusers(chat_id)
    _notes[name] = note


    await authuserdb.update_one(
        {"chat_id": chat_id}, {"$set": {"notes": _notes}}, upsert=True
    )




async def delete_authuser(chat_id: int, name: str) -> bool:
    notesd = await _get_authusers(chat_id)
    name = name
    if name in notesd:
        del notesd[name]
        await authuserdb.update_one(
            {"chat_id": chat_id},
            {"$set": {"notes": notesd}},
            upsert=True,
        )
        return True
    return False




async def get_gbanned() -> list:
    results = []
    async for user in gbansdb.find({"user_id": {"$gt": 0}}):
        user_id = user["user_id"]
        results.append(user_id)
    return results




async def is_gbanned_user(user_id: int) -> bool:
    user = await gbansdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True




async def add_gban_user(user_id: int):
    is_gbanned = await is_gbanned_user(user_id)
    if is_gbanned:
        return
    return await gbansdb.insert_one({"user_id": user_id})




async def remove_gban_user(user_id: int):
    is_gbanned = await is_gbanned_user(user_id)
    if not is_gbanned:
        return
    return await gbansdb.delete_one({"user_id": user_id})




async def get_sudoers() -> list:
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    if not sudoers:
        return []
    return sudoers["sudoers"]




async def add_sudo(user_id: int) -> bool:
    sudoers = await get_sudoers()
    sudoers.append(user_id)
    await sudoersdb.update_one(
        {"sudo": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True
    )
    return True




async def remove_sudo(user_id: int) -> bool:
    sudoers = await get_sudoers()
    sudoers.remove(user_id)
    await sudoersdb.update_one(
        {"sudo": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True
    )
    return True




async def get_banned_users() -> list:
    results = []
    async for user in blockeddb.find({"user_id": {"$gt": 0}}):
        user_id = user["user_id"]
        results.append(user_id)
    return results




async def get_banned_count() -> int:
    users = blockeddb.find({"user_id": {"$gt": 0}})
    users = await users.to_list(length=100000)
    return len(users)




async def is_banned_user(user_id: int) -> bool:
    user = await blockeddb.find_one({"user_id": user_id})
    if not user:
        return False
    return True




async def add_banned_user(user_id: int):
    is_gbanned = await is_banned_user(user_id)
    if is_gbanned:
        return
    return await blockeddb.insert_one({"user_id": user_id})




async def remove_banned_user(user_id: int):
    is_gbanned = await is_banned_user(user_id)
    if not is_gbanned:
        return
    return await blockeddb.delete_one({"user_id": user_id})

async def is_cleanmode_on(chat_id: int) -> bool:
    mode = cleanmode.get(chat_id)
    if not mode:
        user = await cleandb.find_one({"chat_id": chat_id})
        if not user:
            cleanmode[chat_id] = True
            return True
        cleanmode[chat_id] = False
        return False
    return mode


async def cleanmode_on(chat_id: int):
    cleanmode[chat_id] = True
    user = await cleandb.find_one({"chat_id": chat_id})
    if user:
        return await cleandb.delete_one({"chat_id": chat_id})


async def cleanmode_off(chat_id: int):
    cleanmode[chat_id] = False
    user = await cleandb.find_one({"chat_id": chat_id})
    if not user:
        return await cleandb.insert_one({"chat_id": chat_id})


async def is_afk(user_id: int) -> bool:
    user = await afkdb.find_one({"user_id": user_id})
    if not user:
        return False, {}
    return True, user["reason"]


async def add_afk(user_id: int, mode):
    await afkdb.update_one(
        {"user_id": user_id}, {"$set": {"reason": mode}}, upsert=True
    )


async def remove_afk(user_id: int):
    user = await afkdb.find_one({"user_id": user_id})
    if user:
        return await afkdb.delete_one({"user_id": user_id})


async def get_afk_users() -> list:
    users = afkdb.find({"user_id": {"$gt": 0}})
    return list(await users.to_list(length=1000000000)) if users else []

group_types: Iterable[ChatType] = (ChatType.GROUP, ChatType.SUPERGROUP)


async def set_db_lang(chat_id: int, chat_type: str, lang_code: str):
    await localesdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"lang": lang_code, "chat_type": chat_type.value}},
        upsert=True,
    )


async def get_db_lang(chat_id: int) -> str:
    ul = await localesdb.find_one({"chat_id": chat_id})
    return ul["lang"] if ul else {}

# couple store db
async def _get_lovers(chat_id: int):
    lovers = await coupledb.find_one({"chat_id": chat_id})
    if not lovers:
        return {}
    return lovers["couple"]


async def get_couple(chat_id: int, date: str):
    lovers = await _get_lovers(chat_id)
    if date in lovers:
        return lovers[date]
    return False


async def save_couple(chat_id: int, date: str, couple: dict):
    lovers = await _get_lovers(chat_id)
    lovers[date] = couple
    await coupledb.update_one(
        {"chat_id": chat_id},
        {"$set": {"couple": lovers}},
        upsert=True,
    )

 # filters Functions    
async def _get_filters(chat_id: int) -> Dict[str, int]:
    _filters = await filtersdb.find_one({"chat_id": chat_id})
    return _filters["filters"] if _filters else {}


async def delete_filter(chat_id: int, name: str) -> bool:
    filtersd = await _get_filters(chat_id)
    name = name.lower().strip()
    if name in filtersd:
        del filtersd[name]
        await filtersdb.update_one(
            {"chat_id": chat_id},
            {"$set": {"filters": filtersd}},
            upsert=True,
        )
        return True
    return False


async def deleteall_filters(chat_id: int):
    return await filtersdb.delete_one({"chat_id": chat_id})


async def get_filter(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    _filters = await _get_filters(chat_id)
    return _filters[name] if name in _filters else False


async def get_filters_names(chat_id: int) -> List[str]:
    return list(await _get_filters(chat_id))


async def save_filter(chat_id: int, name: str, _filter: dict):
    name = name.lower().strip()
    _filters = await _get_filters(chat_id)
    _filters[name] = _filter
    await filtersdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"filters": _filters}},
        upsert=True,
    )
   
 # warns Functions
async def get_warns_count() -> dict:
    chats_count = 0
    warns_count = 0
    async for chat in warnsdb.find({"chat_id": {"$lt": 0}}):
        for user in chat["warns"]:
            warns_count += chat["warns"][user]["warns"]
        chats_count += 1
    return {"chats_count": chats_count, "warns_count": warns_count}


async def get_warns(chat_id: int) -> Dict[str, int]:
    warns = await warnsdb.find_one({"chat_id": chat_id})
    return warns["warns"] if warns else {}


async def get_warn(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    warns = await get_warns(chat_id)
    if name in warns:
        return warns[name]


async def add_warn(chat_id: int, name: str, warn: dict):
    name = name.lower().strip()
    warns = await get_warns(chat_id)
    warns[name] = warn

    await warnsdb.update_one(
        {"chat_id": chat_id}, {"$set": {"warns": warns}}, upsert=True
    )


async def remove_warns(chat_id: int, name: str) -> bool:
    warnsd = await get_warns(chat_id)
    name = name.lower().strip()
    if name in warnsd:
        del warnsd[name]
        await warnsdb.update_one(
            {"chat_id": chat_id},
            {"$set": {"warns": warnsd}},
            upsert=True,
        )
        return True
    return False
 

async def approve_user(chat_id: int, user_id: int):
    await approve_col.update_one(
        {"chat_id": chat_id},
        {"$addToSet": {"approved_users": user_id}},
        upsert=True
    )

async def disapprove_user(chat_id: int, user_id: int):
    await approve_col.update_one(
        {"chat_id": chat_id},
        {"$pull": {"approved_users": user_id}}
    )

async def is_user_approved(chat_id: int, user_id: int) -> bool:
    chat_data = await approve_col.find_one({"chat_id": chat_id})
    if chat_data and "approved_users" in chat_data:
        return user_id in chat_data["approved_users"]
    return False

async def list_approved_users(chat_id: int) -> list:
    chat_data = await approve_col.find_one({"chat_id": chat_id})
    if chat_data and "approved_users" in chat_data:
        return chat_data["approved_users"]
    return []

async def unapprove_all_users(chat_id: int):
    await approve_col.update_one(
        {"chat_id": chat_id},
        {"$set": {"approved_users": []}}
    )

async def count_approved_users(chat_id: int) -> int:
    chat_data = await approve_col.find_one({"chat_id": chat_id})
    if chat_data and "approved_users" in chat_data:
        return len(chat_data["approved_users"])
    return 0

async def migrate_chat(old_chat_id: int, new_chat_id: int):
    await approve_col.update_one(
        {"chat_id": old_chat_id},
        {"$set": {"chat_id": new_chat_id}}
    )

# Welcome Functions
async def set_welcome_message(chat_id: int, message: str):
    welcome_col.update_one(
        {"chat_id": chat_id},
        {"$set": {"welcome_message": message}},
        upsert=True
    )

async def set_goodbye_message(chat_id: int, message: str):
    welcome_col.update_one(
        {"chat_id": chat_id},
        {"$set": {"goodbye_message": message}},
        upsert=True
    )

async def get_welcome_message(chat_id: int, no_format=False):
    data = welcome_col.find_one({"chat_id": chat_id})
    return data["welcome_message"] if data else None

async def get_goodbye_message(chat_id: int, no_format=False):
    data = welcome_col.find_one({"chat_id": chat_id})
    return data["goodbye_message"] if data else None

async def reset_welcome_message(chat_id: int):
    welcome_col.update_one(
        {"chat_id": chat_id},
        {"$unset": {"welcome_message": ""}}
    )

async def reset_goodbye_message(chat_id: int):
    welcome_col.update_one(
        {"chat_id": chat_id},
        {"$unset": {"goodbye_message": ""}}
    )

async def enable_welcome(chat_id: int):
    welcome_col.update_one(
        {"chat_id": chat_id},
        {"$set": {"welcome_enabled": True}},
        upsert=True
    )

async def disable_welcome(chat_id: int):
    welcome_col.update_one(
        {"chat_id": chat_id},
        {"$set": {"welcome_enabled": False}},
        upsert=True
    )

async def enable_goodbye(chat_id: int):
    welcome_col.update_one(
        {"chat_id": chat_id},
        {"$set": {"goodbye_enabled": True}},
        upsert=True
    )

async def disable_goodbye(chat_id: int):
    welcome_col.update_one(
        {"chat_id": chat_id},
        {"$set": {"goodbye_enabled": False}},
        upsert=True
    )

async def get_welcome_settings(chat_id: int):
    data = welcome_col.find_one({"chat_id": chat_id})
    if data:
        return {
            "welcome_message": data.get("welcome_message"),
            "goodbye_message": data.get("goodbye_message"),
            "clean_welcome": data.get("clean_welcome", False),
            "clean_goodbye": data.get("clean_goodbye", False),
            "clean_service": data.get("clean_service", False),
            "welcome_enabled": data.get("welcome_enabled", True),
            "goodbye_enabled": data.get("goodbye_enabled", True),
        }
    return {}

async def set_cleanwelcome(chat_id: int, status: bool):
    welcome_col.update_one(
        {"chat_id": chat_id},
        {"$set": {"clean_welcome": status}},
        upsert=True
    )

async def set_cleangoodbye(chat_id: int, status: bool):
    welcome_col.update_one(
        {"chat_id": chat_id},
        {"$set": {"clean_goodbye": status}},
        upsert=True
    )

async def get_cleanwelcome_status(chat_id: int):
    data = welcome_col.find_one({"chat_id": chat_id})
    return data.get("clean_welcome", False) if data else False

async def get_cleangoodbye_status(chat_id: int):
    data = welcome_col.find_one({"chat_id": chat_id})
    return data.get("clean_goodbye", False) if data else False

async def set_cleanservice(chat_id: int, status: bool):
    welcome_col.update_one(
        {"chat_id": chat_id},
        {"$set": {"clean_service": status}},
        upsert=True
    )

async def get_cleanservice_status(chat_id: int):
    data = welcome_col.find_one({"chat_id": chat_id})
    return data.get("clean_service", False) if data else False

# Locks Functions
async def lock_chat(chat_id: int, lock_type: str):
    locks_col.update_one(
        {"chat_id": chat_id},
        {"$set": {f"locks.{lock_type}": True}},
        upsert=True
    )

async def unlock_chat(chat_id: int, lock_type: str):
    locks_col.update_one(
        {"chat_id": chat_id},
        {"$set": {f"locks.{lock_type}": False}},
        upsert=True
    )

async def is_chat_locked(chat_id: int, lock_type: str) -> bool:
    data = locks_col.find_one({"chat_id": chat_id})
    return data["locks"].get(lock_type, False) if data and "locks" in data else False
    
    
# feds    
def get_fed_info(fed_id):
    get = fedsdb.find_one({"fed_id": str(fed_id)})
    return False if get is None else get


async def get_fed_id(chat_id):
    get = await fedsdb.find_one({"chat_ids.chat_id": int(chat_id)})

    if get is None:
        return False
    return next(
        (
            get["fed_id"]
            for chat_info in get.get("chat_ids", [])
            if chat_info["chat_id"] == int(chat_id)
        ),
        False,
    )


async def get_feds_by_owner(owner_id):
    cursor = fedsdb.find({"owner_id": owner_id})
    feds = await cursor.to_list(length=None)
    if not feds:
        return False
    return [
        {"fed_id": fed["fed_id"], "fed_name": fed["fed_name"]} for fed in feds
    ]


async def transfer_owner(fed_id, current_owner_id, new_owner_id):
    if await is_user_fed_owner(fed_id, current_owner_id):
        await fedsdb.update_one(
            {"fed_id": fed_id, "owner_id": current_owner_id},
            {"$set": {"owner_id": new_owner_id}},
        )
        return True
    else:
        return False


async def set_log_chat(fed_id, log_group_id: int):
    await fedsdb.update_one(
        {"fed_id": fed_id}, {"$set": {"log_group_id": log_group_id}}
    )
    return


async def get_fed_name(chat_id):
    get = await fedsdb.find_one(int(chat_id))
    return False if get is None else get["fed_name"]


async def is_user_fed_owner(fed_id, user_id: int):
    getfed = await get_fed_info(fed_id)
    if not getfed:
        return False
    owner_id = getfed["owner_id"]
    return user_id == owner_id or user_id not in OWNER_ID


async def search_fed_by_id(fed_id):
    get = await fedsdb.find_one({"fed_id": str(fed_id)})

    return get if get is not None else False


def chat_join_fed(fed_id, chat_name, chat_id):
    return fedsdb.update_one(
        {"fed_id": fed_id},
        {"$push": {"chat_ids": {"chat_id": int(chat_id), "chat_name": chat_name}}},
    )


async def chat_leave_fed(chat_id):
    result = await fedsdb.update_one(
        {"chat_ids.chat_id": int(chat_id)},
        {"$pull": {"chat_ids": {"chat_id": int(chat_id)}}},
    )
    return result.modified_count > 0


async def user_join_fed(fed_id, user_id):
    result = await fedsdb.update_one(
        {"fed_id": fed_id}, {"$addToSet": {"fadmins": int(user_id)}}, upsert=True
    )
    return result.modified_count > 0


async def user_demote_fed(fed_id, user_id):
    result = await fedsdb.update_one(
        {"fed_id": fed_id}, {"$pull": {"fadmins": int(user_id)}}
    )
    return result.modified_count > 0


async def search_user_in_fed(fed_id, user_id):
    getfed = await search_fed_by_id(fed_id)
    return False if getfed is None else user_id in getfed["fadmins"]


async def chat_id_and_names_in_fed(fed_id):
    getfed = await search_fed_by_id(fed_id)

    if getfed is None or "chat_ids" not in getfed:
        return [], []

    chat_ids = [chat["chat_id"] for chat in getfed["chat_ids"]]
    chat_names = [chat["chat_name"] for chat in getfed["chat_ids"]]
    return chat_ids, chat_names


async def add_fban_user(fed_id, user_id, reason):
    current_date = datetime.now(pytz.timezone("Asia/Jakarta")).strftime(
        "%Y-%m-%d %H:%M"
    )
    await fedsdb.update_one(
        {"fed_id": fed_id},
        {
            "$push": {
                "banned_users": {
                    "user_id": int(user_id),
                    "reason": reason,
                    "date": current_date,
                }
            }
        },
        upsert=True,
    )


async def remove_fban_user(fed_id, user_id):
    await fedsdb.update_one(
        {"fed_id": fed_id}, {"$pull": {"banned_users": {"user_id": int(user_id)}}}
    )


async def check_banned_user(fed_id, user_id):
    result = await fedsdb.find_one({"fed_id": fed_id, "banned_users.user_id": user_id})
    if result and "banned_users" in result:
        for user in result["banned_users"]:
            if user.get("user_id") == user_id:
                return {"reason": user.get("reason"), "date": user.get("date")}

    return False
