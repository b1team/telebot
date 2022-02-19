from aiogram import types
from aiogram.types import ReplyKeyboardMarkup

keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True,
                                one_time_keyboard=True).add("👋 Hello!")


async def welcome(message: types.Message):
    name = message['from'].first_name + ' ' + message['from'].last_name
    await message.reply(
        f"Chào mừng {name} đến với chatbot được tạo bởi sinh viên D13CNPM4",
        reply_markup=keyboard1)


"""
example:
{"message_id": 220,
    "from": {"id": 1004137626, "is_bot": false,
            "first_name": "Falcol", "last_name": "l",
                "username": "FalColl", "language_code": "en"},
    "chat": {"id": 1004137626, "first_name": "Falcol",
            "last_name": "l", "username": "FalColl",
            "type": "private"},
    "date": 1643350793,
    "text": "hi"}"""
