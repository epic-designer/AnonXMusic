from typing import Union
from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, CallbackQuery,Message

from AnonXMusic import app
from AnonXMusic.utils import help_pannel
from AnonXMusic.utils.database import get_lang
from AnonXMusic.utils.decorators.language import LanguageStart, languageCB
from AnonXMusic.utils.inline.help import help_back_markup, private_help_panel
from config import BANNED_USERS, SUPPORT_CHAT
from AnonXMusic.utils.paginateFn import generate_help_buttons

from strings import get_string, helpers

@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(client: app, update: Union[types.Message, types.CallbackQuery]):
    if isinstance(update, CallbackQuery):
        await update.answer()
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = generate_help_buttons(page=0)
        await update.edit_message_text(
            _["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard
        )
    elif isinstance(update, types.Message):
        try:
            await update.delete()
        except:
            pass
        language = await get_lang(update.chat.id)
        _ = get_string(language)
        keyboard = generate_help_buttons(page=0)
        await update.reply_text(
            text=_["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard
        )

@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))

@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = help_back_markup(_)
    help_texts = {
        "hb1": helpers.HELP_1,
        "hb2": helpers.HELP_2,
        "hb6": helpers.HELP_6,
        "hb8": helpers.HELP_8,
        "hb11": helpers.HELP_11,
        "hb12": helpers.HELP_12,
        "hb13": helpers.HELP_13,
        "hb14": helpers.HELP_14,
        "hb15": helpers.HELP_15
    }
    if cb in help_texts:
        await CallbackQuery.edit_message_text(help_texts[cb], reply_markup=keyboard)

@app.on_callback_query(filters.regex("helpT") & ~BANNED_USERS)
async def helper_private(client: app, update: Union[types.Message, types.CallbackQuery]):
    if isinstance(update, CallbackQuery):
        await update.answer()
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = help_pannel(_, True)
        await update.edit_message_text(
            _["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard
        )
    elif isinstance(update, types.Message):
        try:
            await update.delete()
        except:
            pass
        language = await get_lang(update.chat.id)
        _ = get_string(language)
        keyboard = help_pannel(_, True)
        await update.reply_text(
            text=_["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard
        )
