from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from model.train_model_v3 import classify, response
from utils.database import find_student_id

keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True,
                                one_time_keyboard=True).add("👋 Hello!")


async def welcome(message: types.Message):
    name = message['from'].first_name + ' ' + message['from'].last_name
    await message.reply(
        f"Chào mừng {name} đến với chatbot được tạo bởi sinh viên D13CNPM4",
        reply_markup=keyboard1)


async def kb_answer(message: types.Message):
    if message.text == 'Xin lịch thi' or message.text == 'Xin lịch học':
        try:
            student = await find_student_id(message['from'].username)
        except Exception as e:
            await message.reply(f'Lỗi khi lấy msv: {e}')
            return

        if not student:
            text = "Bạn vẫn chưa lấy lịch\nHãy gõ theo lệnh\n"\
                    "/msv 188xxxxxxxx\n để lấy thông tin"
            await message.reply(text)
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
