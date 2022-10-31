from aiogram import executor
from create_bot import dp

async def on_statup(_):
    print("Bot started")

from handlers import client

client.register_handlers_client(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_statup)


