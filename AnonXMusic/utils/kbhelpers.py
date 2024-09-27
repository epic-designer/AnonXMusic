from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def to_small_caps(text):
    normal = "abcdefghijklmnopqrstuvwxyz"
    small_caps = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘϙʀsᴛᴜᴠᴡxʏᴢ"
    translation_table = str.maketrans(normal, small_caps)
    text = text.capitalize()  # Ensures the first letter is capitalized
    return text[0] + text[1:].translate(translation_table)

def ikb(rows=None, back=False, todo="settingsback_helper"):
    """ rows = pass the rows
    back - if want to make back button
    todo - callback data of back button
    """
    if rows is None:
        rows = []
    lines = []
    try:
        for row in rows:
            line = []
            for button in row:
                if '.' in button:
                    btn_text1 = button.split(".")[1]
                    btn_text = to_small_caps(btn_text1)  # Convert text to small caps
                    button = btn(btn_text, button)  # InlineKeyboardButton
                else:
                    button = btn(*button)  # Will make the kb which don't have "." in them
                line.append(button)
            lines.append(line)
    except AttributeError:
        # Handle cases where button format might not match expected format
        for row in rows:
            line = []
            for button in row:
                button = btn(*button)  # InlineKeyboardButton
                line.append(button)
            lines.append(line)
    except TypeError:
        # Handle cases where rows might be a flat list
        line = []
        for button in rows:
            button = btn(*button)  # InlineKeyboardButton
            line.append(button)
        lines.append(line)
    if back: 
        back_btn = [btn("BACK", todo)]
        lines.append(back_btn)
    return InlineKeyboardMarkup(inline_keyboard=lines)

def btn(text, value, type="callback_data"):
    return InlineKeyboardButton(text, **{type: value})
