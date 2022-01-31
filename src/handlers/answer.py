from aiogram import types
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           ReplyKeyboardMarkup)
from model.train_model_v3 import classify, response
from utils.database import find_student_id
from utils.supports import get_all_dates_of_week

keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True,
                                one_time_keyboard=True).add(
                                    "👋 Hello!", "Lap trinh python",
                                    "ngon ngu kich ban",
                                    "Kiem thu va dam bao chat luong phan mem")


def get_keyboard() -> InlineKeyboardMarkup:

    markup = InlineKeyboardMarkup(resize_keyboard=True)
    for title, day in get_all_dates_of_week():
        markup.add(InlineKeyboardButton(text=title, callback_data=day))
    return markup


async def random_answer(message: types.Message):
    await message.reply("Select a range:", reply_markup=get_keyboard())


async def welcome(message: types.Message):
    name = message['from'].first_name + ' ' + message['from'].last_name
    await message.reply(
        f"Chào mừng {name} đến với chatbot được tạo bởi sinh viên D13CNPM4",
        reply_markup=keyboard1)


async def random_value(call: types.CallbackQuery):
    days = [day for _, day in get_all_dates_of_week()]
    names = [title for title, _ in get_all_dates_of_week()]
    if call.data in days:
        await call.message.answer(f"{names[days.index(call.data)]} {call.data}"
                                  )
    await call.answer()


async def kb_answer(message: types.Message):
    if message.text == 'Xin lịch thi' or message.text == 'Xin lịch học':
        try:
            student = await find_student_id(message['from'].username)
        except Exception as e:
            await message.reply(f'Lỗi khi lấy msv: {e}')
            return

        if not student:
            await message.reply("""Bạn vẫn chưa lấy lịch\nHãy gõ theo lệnh
                            /msv 188xxxxxxxx\n để lấy thông tin""")
            return
        else:
            await message.reply(
                'Lịch đã được lấy về, bạn có thể gõ /info để xem cách sử dụng')
            return
    else:
        tag, _ = classify(message.text)
        await message.reply(response(tag))


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
