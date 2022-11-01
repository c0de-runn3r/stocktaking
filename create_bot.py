from aiogram import Bot, Dispatcher
from config import API_TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

def get_username_list():
    file = open('tg_usernames.txt', 'r+')
    username_list = file.read().split('\n')
    file.close()
    return username_list

def add_username(username):
    file = open('tg_usernames.txt', 'r+')
    file.seek(0, 2)
    file.write(username + "\n")
    file.close()
    return "Користувач {} успішно доданий!".format(username)
