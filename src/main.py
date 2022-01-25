from aiogram import Dispatcher, executor
from bot import dp
from handlers import *
from aiogram.types import BotCommand

async def start_up(dispatcher: Dispatcher):
    setup(dispatcher)

    # goi y command [BotCommand('TEN_COMMAND', 'PLALCE HOLDER')]
    await dp.bot.set_my_commands([BotCommand('start', 'hello start')])


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=start_up)
