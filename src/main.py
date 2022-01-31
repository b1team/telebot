from aiogram import Dispatcher, executor
from bot import dp
from handlers import setup
from aiogram.types import BotCommand


# from src.model.train_model_v3 import train_model
async def start_up(dispatcher: Dispatcher):
    setup(dispatcher)

    # goi y command [BotCommand('TEN_COMMAND', 'PLALCE HOLDER')]
    await dp.bot.set_my_commands([
        BotCommand('start', 'Xin chào'),
        BotCommand('info', 'Thông tin cách dùng'),
        # BotCommand('find', 'Tìm lịch học: /find 01-02-2022'),
        # BotCommand('msv', 'Lấy thông tin msv: /msv 188xxxxxxxx'),
    ])


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=start_up)
