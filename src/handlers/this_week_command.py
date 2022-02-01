from aiogram import types
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)

from utils.database import find_student_id, find_one_timetable
from utils.supports import get_all_dates_of_week


def get_keyboard() -> InlineKeyboardMarkup:

    markup = InlineKeyboardMarkup(resize_keyboard=True)
    for title, day in get_all_dates_of_week():
        markup.add(InlineKeyboardButton(text=title, callback_data=day))
    return markup


async def this_week_dates(message: types.Message):
    await message.reply("Lịch tuần này:", reply_markup=get_keyboard())


async def this_week(call: types.CallbackQuery):
    date = call.data
    try:
        student_id = await find_student_id(call['from'].username)
    except Exception as e:
        await call.message.answer(f'Lỗi khi lấy msv: {e}')
        return

    if student_id is None:
        text = 'Bạn chưa lấy dữ liệu thời khóa biểu\n'\
               'Dùng /info để biết thêm chi tiết'
        await call.message.answer(text)
        return
    else:
        try:
            timetable = await find_one_timetable(date, student_id)
        except Exception as e:
            await call.message.answer(f'Lỗi khi lấy thời khóa biểu: {e}')
        if timetable == []:
            await call.message.answer(f'Không có lịch học ngày {date}')
        else:
            for i in timetable:
                info = \
                        "---------------------------------\n"\
                        f"{i['weekday']}, {i['date_start']}\n"\
                        f"Msv: {i['student_id']}\n"\
                        f"Lớp học: {i['classroom']}\n"\
                        f"Môn học: {i['subject'][:i['subject'].find('(')]}\n"\
                        f"Tiết học: {i['class_time']}\n"\
                        f"Giờ học: {i['time_start']}\n"\
                        f"Giáo viên: {i['teacher']}\n"\
                        "---------------------------------\n"
                await call.message.answer(info)
