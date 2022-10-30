from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from connect_db import get_table_list
from stock import allowed_actions_list

# actions keyboard
kb_actions = InlineKeyboardMarkup()

for act in allowed_actions_list:
    act = InlineKeyboardButton(act, callback_data=act)
    kb_actions.add(act)

# sections keyboard
kb_sections = InlineKeyboardMarkup()

for section in get_table_list():
    section = InlineKeyboardButton(section, callback_data=section)
    kb_sections.add(section)


