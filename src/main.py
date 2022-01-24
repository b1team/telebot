from aiogram import Dispatcher, executor
from bot import dp
from src import handlers
from aiogram.types import BotCommand
from src.model.train_model import train_model

async def start_up(dispatcher: Dispatcher):
    handlers.setup(dispatcher)

    # goi y command [BotCommand('TEN_COMMAND', 'PLALCE HOLDER')]
    await dp.bot.set_my_commands([BotCommand('start', 'hello start')])


if __name__ == '__main__':
    train_model()
    executor.start_polling(dp, on_startup=start_up)
