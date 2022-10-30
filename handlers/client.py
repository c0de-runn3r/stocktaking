from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from connect_db import get_table_list, get_item_list
from stock import allowed_actions_list, get_element_quantity, update_element_quantuty_take, update_element_quantuty_put
from buttons.buttons import kb_actions, kb_sections

class FSMAdmin(StatesGroup):
    action_state = State()
    section_state = State()
    item_state = State()
    quantity_state = State()

# start handlers
# @dp.register_message_handler(commands=['start'], state=None)
async def process_start_command(message: types.Message):
    await FSMAdmin.action_state.set()
    await message.answer("Привіт!\nЯ бот-помічник для менеджерів Маку!\nНапиши дію для виконання.\nЯ знаю такі дії:", reply_markup=kb_actions)

# Action handlers in here
# @dp.message_handler(Text(equals=allowed_actions_list, ignore_case=True), state=FSMAdmin.action_state)
async def get_action(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['action'] = message.text
    await FSMAdmin.next()
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
    await FSMAdmin.next()
    await message.answer("Тепер вибери предмет.\nЄ такі предмети:\n" + ('\n'.join(map(str, list(get_item_list(data['section']).values())))))

# @dp.message_handler(state=FSMAdmin.section_state)
async def get_section_err(message: types.Message, state: FSMContext):
    await FSMAdmin.section_state.set()
    await message.answer("Немає такого розділу, спробуй ще раз.")

# Items handlers in here
# @dp.message_handler(state=FSMAdmin.item_state)
async def get_item(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['item'] = message.text
    await FSMAdmin.next()
    await message.answer("Тепер введи кількість.")

# Quantity handlers in here
# @dp.message_handler(state=FSMAdmin.quantity_state)
async def get_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['quantity'] = int(message.text)
    async with state.proxy() as data:
        if data['action'] == 'Взяти':
            new_quantity = update_element_quantuty_take(data['section'], data['item'], get_element_quantity(data['section'], data['item']), data['quantity'])
            await message.answer("Успішно. Нова кількість елемента: " + data['item'] + " складає " + str(new_quantity) + " одиниць.")
        elif data['action'] == 'Покласти':
            new_quantity = update_element_quantuty_put(data['section'], data['item'], get_element_quantity(data['section'], data['item']), data['quantity'])
            await message.answer("Успішно. Нова кількість елемента: " + data['item'] + " складає " + str(new_quantity) + " одиниць.")
    await state.finish()

# Cancel handlers in here
# @dp.message_handler(Text(equals="відміна", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Окей. Відміна.")

# register handlers
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(process_start_command, commands=['start'], state=None)
    dp.register_message_handler(cancel_handler, Text(equals="відміна", ignore_case=True), state="*")
    dp.register_message_handler(get_action, Text(equals=allowed_actions_list, ignore_case=True), state=FSMAdmin.action_state)
    dp.register_message_handler(get_action_err, state=FSMAdmin.action_state)
    dp.register_message_handler(get_section, Text(equals=get_table_list(), ignore_case=True), state=FSMAdmin.section_state)
    dp.register_message_handler(get_section_err, state=FSMAdmin.section_state)
    dp.register_message_handler(get_item, state=FSMAdmin.item_state)
    dp.register_message_handler(get_quantity, state=FSMAdmin.quantity_state)
    
    
