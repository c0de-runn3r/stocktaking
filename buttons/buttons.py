from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

from connect_db import get_table_list
from stock import allowed_actions_list

# cancel button
cancel_bttn = KeyboardButton("❌ Відміна ❌")

# actions keyboard
kb_actions = ReplyKeyboardMarkup(resize_keyboard=True)

for act in allowed_actions_list:
    act = KeyboardButton(act)
    kb_actions.add(act)
kb_actions.add(cancel_bttn)

# sections keyboard
kb_sections = ReplyKeyboardMarkup(resize_keyboard=True)

for section in get_table_list():
    section = KeyboardButton(section)
    kb_sections.add(section)
kb_sections.add(cancel_bttn)

# items keyboard were moved to handlers.client because of unability to do paralell import

