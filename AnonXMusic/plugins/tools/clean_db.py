import time
from asyncio import sleep
from traceback import format_exc

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.errors import PeerIdInvalid, UserNotParticipant

from AnonXMusic import LOGGER, TIME_ZONE, app
from AnonXMusic.database.approve_db import Approve
from AnonXMusic.database.blacklist_db import Blacklist
from AnonXMusic.database.chats_db import Chats
from AnonXMusic.database.disable_db import Disabling
from AnonXMusic.database.filters_db import Filters
from AnonXMusic.database.flood_db import Floods
from AnonXMusic.database.greetings_db import Greetings
from AnonXMusic.database.notes_db import Notes, NotesSettings
from AnonXMusic.database.pins_db import Pins
from AnonXMusic.database.reporting_db import Reporting
# from AnonXMusic.database.users_db import Users
from AnonXMusic.database.warns_db import Warns, WarnSettings
from AnonXMusic.utils.custom_filters import command
import config as Config


async def clean_my_db(c:app,is_cmd=False, id=None):
    to_clean = list()
    chats_list = Chats.list_chats_by_id()
    to_clean.clear()
    start = time.time()
    for chats in chats_list:
        try:
            stat = await c.get_chat_member(chat_id=chats,user_id=Config.BOT_ID)
            if stat.status not in [CMS.MEMBER, CMS.ADMINISTRATOR, CMS.OWNER]:
                to_clean.append(chats)
        except UserNotParticipant:
            to_clean.append(chats)
        except Exception as e:
            LOGGER(__name__).error(e)
            LOGGER(__name__).error(format_exc())
            if not is_cmd:
                return e
            else:
                to_clean.append(chats)
    for i in to_clean:
        Approve(i).clean_approve()
        Blacklist(i).clean_blacklist()
        Chats.remove_chat(i)
        Disabling(i).clean_disable()
        Filters().rm_all_filters(i)
        Floods().rm_flood(i)
        Greetings(i).clean_greetings()
        Notes().rm_all_notes(i)
        NotesSettings().clean_notes(i)
        Pins(i).clean_pins()
        Reporting(i).clean_reporting()
        Warns(i).clean_warn()
        WarnSettings(i).clean_warns()
    x = len(to_clean)
    txt = f"#INFO\n\nCleaned db:\nTotal chats removed: {x}"
    to_clean.clear()
    nums = time.time()-start
    if is_cmd:
        txt += f"\nClean type: Forced\nInitiated by: {(await c.get_users(user_ids=id)).mention}"
        txt += f"\nClean type: Manual\n\tTook {round(nums,2)} seconds to complete the process"
        await c.send_message(chat_id=Config.LOGGER_ID,text=txt)
        return txt
    else:
        txt += f"\nClean type: Auto\n\tTook {round(nums,2)} seconds to complete the process"
        await c.send_message(chat_id=Config.LOGGER_ID,text=txt)
        return txt
    


