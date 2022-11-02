from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from create_bot import get_username_list, add_username
from connect_db import get_table_list, get_item_list, get_item_list_with_quantity
from stock import add_new_item, allowed_actions_list, get_element_quantity, update_element_quantuty_take, update_element_quantuty_put
from buttons.buttons import kb_actions, kb_sections, cancel_bttn, kb_actions_add_user

class FSMAdmin(StatesGroup):
    action_state = State()
    section_state = State()
    item_state = State()
    quantity_state = State()
    wrin_state = State()
    location_state = State()
    username_state = State()

# start handlers
# @dp.register_message_handler(commands=['start'], state=None)
async def process_start_command(message: types.Message):
    user_name = message.from_user.username
    if user_name in get_username_list():
        await FSMAdmin.action_state.set()
        await message.answer("Привіт!\nЯ бот-помічник для менеджерів Маку!\nНапиши дію для виконання.\nЯ знаю такі дії:", reply_markup=kb_actions)
    elif user_name == "valeryostapenko":
        await FSMAdmin.action_state.set()
        await message.answer("Привіт!\nЯ бот-помічник для менеджерів Маку!\nНапиши дію для виконання.\nЯ знаю такі дії:", reply_markup=kb_actions_add_user)
    else:
        await message.answer("Немає доступу!\nЗверніться до @valeryostapenko")

# Action handlers in here
# @dp.message_handler(Text(equals=allowed_actions_list, ignore_case=True), state=FSMAdmin.action_state)
async def get_action(message: types.Message, state: FSMContext):
    user_name = message.from_user.username
    async with state.proxy() as data:
        data['action'] = message.text
    if data['action'] == "Додати користувача":
        if user_name == "valeryostapenko":
            await FSMAdmin.username_state.set()
            await message.answer("Введи username (без символа @):")
        else:
            await FSMAdmin.action_state.set()
            await message.answer("Немає доступу для цієї дії.\nЗверніться до @valeryostapenko", reply_markup=kb_actions)
    else:
        await FSMAdmin.section_state.set()
        await message.answer("Тепер вибери розділ.\nЄ такі розділи:", reply_markup=kb_sections)

# @dp.message_handler(state=FSMAdmin.action_state)
async def get_action_err(message: types.Message, state: FSMContext):
    await FSMAdmin.action_state.set()
    await message.answer("Не знаю такої дії, спробуй ще раз.")

# Section handlers in here
# @dp.message_handler(Text(equals=table_list, ignore_case=True), state=FSMAdmin.section_state)
async def get_section(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['section'] = message.text
    if data['action'] == "Додати новий предмет":
        await FSMAdmin.item_state.set()
        await message.answer("Напиши назву предмета:")
    elif data['action'] == "Показати загальну кількість":
        await FSMAdmin.action_state.set()
        await message.answer(get_item_list_with_quantity(data['section']), reply_markup=kb_actions)
    else:
        kb_items = ReplyKeyboardMarkup(one_time_keyboard=True)
        for item in get_item_list(data['section']):
            item = KeyboardButton(item)
            kb_items.add(item)
        kb_items.add(cancel_bttn)
        await FSMAdmin.item_state.set()
        await message.answer("Тепер вибери предмет.\nЄ такі предмети:", reply_markup=kb_items)

# @dp.message_handler(state=FSMAdmin.section_state)
async def get_section_err(message: types.Message, state: FSMContext):
    await FSMAdmin.section_state.set()
    await message.answer("Немає такого розділу, спробуй ще раз.")

# Items handlers in here
# @dp.message_handler(state=FSMAdmin.item_state)
async def get_item(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['item'] = message.text
    if data['action'] == 'Додати новий предмет':
        await FSMAdmin.wrin_state.set()
        await message.answer("Тепер введи WRIN:")
    else:
        await FSMAdmin.quantity_state.set()
        await message.answer("Тепер введи кількість:")

# Quantity handlers in here
# @dp.message_handler(state=FSMAdmin.quantity_state)
async def get_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['quantity'] = int(message.text)
    async with state.proxy() as data:
        if data['action'] == 'Взяти':
            if get_element_quantity(data['section'], data['item']) < data['quantity']:
                await message.answer("Не можна взяти більше '{}', аніж є на складі ({})".format(data['item'], get_element_quantity(data['section'], data['item'])))
                await FSMAdmin.quantity_state.set()
            else:
                new_quantity = update_element_quantuty_take(data['section'], data['item'], get_element_quantity(data['section'], data['item']), data['quantity'])
                await message.answer("Успішно. Нова кількість елемента: " + data['item'] + " складає " + str(new_quantity) + " одиниць.", reply_markup=kb_actions)
                await FSMAdmin.action_state.set()
        elif data['action'] == 'Покласти':
            new_quantity = update_element_quantuty_put(data['section'], data['item'], get_element_quantity(data['section'], data['item']), data['quantity'])
            await message.answer("Успішно. Нова кількість елемента: " + data['item'] + " складає " + str(new_quantity) + " одиниць.", reply_markup=kb_actions)
            await FSMAdmin.action_state.set()
        elif data['action'] == 'Додати новий предмет':
            msg = add_new_item(data['section'], data['wrin'], data['item'], data['quantity'], data['location'])
            await message.answer(msg, reply_markup=kb_actions)
            await FSMAdmin.action_state.set()

async def get_quantity_err(message: types.Message):
    await message.answer("Краще вказати кількість цифрами)")
    await FSMAdmin.quantity_state.set()


# wrin handlers in here
# @dp.message_handler(state=FSMAdmin.wrin_state)
async def get_wrin(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['wrin'] = message.text
    await FSMAdmin.location_state.set()
    await message.answer("Тепер вкажи локацію (де зберігається цей предмет):")

# location handlers in here
# @dp.message_handler(state=FSMAdmin.location_state)
async def get_location(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['location'] = message.text
    await FSMAdmin.quantity_state.set()
    await message.answer("Тепер вкажи кількість:")

# username handlers in here
# @dp.message_handler(state=FSMAdmin.username_state)
async def get_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
    if message.from_user.username == "valeryostapenko":
        await FSMAdmin.action_state.set()
        await message.answer(add_username(data['username']), reply_markup=kb_actions)
    else:
        await FSMAdmin.action_state.set()
        await message.answer("Немає доступу для цієї дії.\nЗверніться до @valeryostapenko", reply_markup=kb_actions)

# Cancel handlers in here
# @dp.message_handler(Text(equals="відміна", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await FSMAdmin.action_state.set()
    await message.answer("Окей. Відміна.", reply_markup=kb_actions)

# register handlers
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(process_start_command, commands=['start'], state=None)
    dp.register_message_handler(cancel_handler, Text(equals="❌ Відміна ❌", ignore_case=True), state="*")
    dp.register_message_handler(get_action, Text(equals=allowed_actions_list, ignore_case=True), state=FSMAdmin.action_state)
    dp.register_message_handler(get_action_err, state=FSMAdmin.action_state)
    dp.register_message_handler(get_section, Text(equals=get_table_list(), ignore_case=True), state=FSMAdmin.section_state)
    dp.register_message_handler(get_section_err, state=FSMAdmin.section_state)
    dp.register_message_handler(get_item, state=FSMAdmin.item_state)
    dp.register_message_handler(get_wrin, state=FSMAdmin.wrin_state)
    dp.register_message_handler(get_location,state=FSMAdmin.location_state)
    dp.register_message_handler(get_quantity, regexp='^[0-9]+', state=FSMAdmin.quantity_state)
    dp.register_message_handler(get_quantity_err, state=FSMAdmin.quantity_state)
    dp.register_message_handler(get_username, state=FSMAdmin.username_state)
    
    
