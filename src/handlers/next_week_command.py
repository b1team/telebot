from aiogram import types
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)

from utils.database import find_student_id, find_one_timetable
from utils.supports import get_all_dates_of_week


def get_keyboard() -> InlineKeyboardMarkup:

    markup = InlineKeyboardMarkup(resize_keyboard=True)
    for title, day in get_all_dates_of_week(7):
        markup.add(InlineKeyboardButton(text=title, callback_data=day))
    return markup


async def next_week_dates(message: types.Message):
    await message.reply("Lịch tuần sau:", reply_markup=get_keyboard())


async def this_week(call: types.CallbackQuery):
    date = call.data
    try:
        student_id = await find_student_id(call['from'].username)
    except Exception as e:
        await call.reply(f'Lỗi khi lấy msv: {e}')
        return

    if student_id is None:
        await call.answer('''Bạn chưa lấy dữ liệu thời khóa biểu
                            Dùng /info để biết thêm chi tiết''')
        return
    else:
        try:
            timetable = await find_one_timetable(date, student_id)
        except Exception as e:
            await call.reply(f'Lỗi khi lấy thời khóa biểu: {e}')
        if timetable == []:
            await call.answer('Không có lịch học')
        else:
            text = ''
            for i in timetable:
                info = f"""
                ---------------------------------
                {i['weekday']}, {i['date_start']}
                Msv: {i['student_id']}
                Lớp học: {i['classroom']}
                Môn học: {i['subject'][:i['subject'].find('(')]}
                Tiết học: {i['class_time']}
                Giờ học: {i['time_start']}
                Giáo viên: {i['teacher']}
                ---------------------------------
                """
                text = text + info
            await call.answer(text)
