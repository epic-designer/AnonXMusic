from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode
import config
import config as Config
from ..logging import LOGGER
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class Anony(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot...")
        super().__init__(
            name="AnonXMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            plugins=dict(root="Powers.plugins", exclude=config.NO_LOAD),
            in_memory=True,   
            max_concurrent_transmissions=7,
            workers=config.WORKERS,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        # Debug print to check the LOGGER_ID value
        print(f"LOGGER_ID: {config.LOGGER_ID}")

        # Attempt to send a message to the chat ID first
        try:
            meh = await self.get_me()
            Config.BOT_ID = meh.id
            Config.BOT_NAME = meh.first_name
            Config.BOT_USERNAME = meh.username        
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b><u>\n\nɪᴅ : <code>{self.id}</code>\nɴᴀᴍᴇ : {self.name}\nᴜsᴇʀɴᴀᴍᴇ : @{self.username}",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid, ValueError) as e:
            LOGGER(__name__).warning(
                f"Failed to send message to chat ID {config.LOGGER_ID}. Trying with group username.\n  Reason: {type(e).__name__}."
            )

            # Attempt to send the message to the group username
            try:
                await self.send_message(
                    chat_id=f"@{config.GROUP_USERNAME}",
                    text=f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b><u>\n\nɪᴅ : <code>{self.id}</code>\nɴᴀᴍᴇ : {self.name}\nᴜsᴇʀɴᴀᴍᴇ : @{self.username}",
                )
            except Exception as ex:
                LOGGER(__name__).error(
                    f"Bot has failed to access the log group/channel.\n  Reason : {type(ex).__name__}."
                )
                exit()

        try:
            a = await self.get_chat_member(config.LOGGER_ID, self.id)
            if a.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error(
                    "Please promote your bot as an admin in your log group/channel."
                )
                exit()
        except Exception as ex:
            LOGGER(__name__).error(
                f"Failed to verify bot's admin status.\n  Reason : {type(ex).__name__}."
            )
            exit()

        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()
