from pyrogram.enums import MessageEntityType
from pyrogram.types import Message, User

from AnonXMusic import app


async def extract_user(m: Message) -> User:
    if m.reply_to_message:
        return m.reply_to_message.from_user
    msg_entities = m.entities[1] if m.text.startswith("/") else m.entities[0]
    return await app.get_users(
        msg_entities.user.id
        if msg_entities.type == MessageEntityType.TEXT_MENTION
        else int(m.command[1])
        if m.command[1].isdecimal()
        else m.command[1]
    )


async def extract_user2(message: Message):
    msg_entities = message.entities or []
    if message.text and message.text.startswith("/") and len(msg_entities) > 1:
        user_entity = msg_entities[1]
    elif len(msg_entities) > 0:
        user_entity = msg_entities[0]
    else:
        return None  # or raise an appropriate error

    if user_entity.type == "text_mention":
        return user_entity.user
    elif user_entity.type == "mention":
        username = message.text[user_entity.offset:user_entity.offset + user_entity.length]
        return await message.chat.get_member(username)

    return message.from_user