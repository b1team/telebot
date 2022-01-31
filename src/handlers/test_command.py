from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from utils.database import (find_one_testtable, find_all_testtable,
                            find_student_id)


def markup_keyboard(testtable: list) -> ReplyKeyboardMarkup:
    # if testtable is empty, return None
    # get all subject from testtable then add to ReplyKeyboardMarkup
    # return ReplyKeyboardMarkup
    global title
    title = []
    if testtable == []:
        markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True).add("Không có lịch thi")
        return markup
    else:
        for i in testtable:
            title.append(i['subject'])
        markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                     one_time_keyboard=True)
        for title in set(title):
            markup.add(title)

        return markup


async def get_markup(message: types.Message):
    try:
        student_id = await find_student_id(message['from'].username)
    except Exception as e:
        await message.reply(f'Lỗi khi lấy msv: {e}')
        return

    if student_id is None:
        await message.answer('''Bạn chưa lấy dữ liệu thời khóa biểu
                                Dùng /info để biết thêm chi tiết''')
        return
    # find_all_testtable, if testtable is empty, reply message and return
    # if testtable is not empty, get all subject from testtable then add to markup_keyboard
    # return markup_keyboard
    try:
        testtable = await find_all_testtable(student_id)
    except Exception as e:
        await message.reply(f'Lỗi khi lấy lịch thi: {e}')
    if testtable == []:
        await message.reply('Không có lịch thi')
        return
    else:
        markup = markup_keyboard(testtable)
        await message.reply('Chọn môn thi', reply_markup=markup)


async def show_testtable(message: types.Message):
    # if message text in title, find_one_testtables and reply message
    # else reply message and return
    # return
    if message.text in title:
        try:
            student_id = await find_student_id(message['from'].username)
        except Exception as e:
            await message.reply(f'Lỗi khi lấy msv: {e}')
            return

        try:
            testtable = await find_one_testtable(message.text, student_id)
        except Exception as e:
            await message.reply(f'Lỗi khi lấy lịch thi: {e}')
        if testtable == []:
            await message.reply('Không có lịch thi')
            return
        else:
            text = ''
            for i in testtable:
                info = f"""
                ---------------------------------
                {i['date']}
                Msv: {i['student_id']}
                Lớp thi: {i['room']}
                Môn thi: {i['subject']}
                Tiết thi: {i['time']}
                Giờ thi: {i['time_start']}
                ---------------------------------
                """
                text = text + info
            await message.reply(text)
    else:
        await message.reply('''Không có lịch thi
               Có thể chạy /test để cập nhập các môn thi nếu đã có
               Nếu không có môn thi có thể là chưa có lịch thi
               Gõ `/info` đẻ biết thêm chi tiết cách lấy dữ liệu''')
