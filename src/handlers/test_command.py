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


def get_subject(testtable: list):
    title = []
    for i in testtable:
        title.append(i['subject'])

    return title


async def get_markup(message: types.Message):
    try:
        student_id = await find_student_id(message['from'].username)
    except Exception as e:
        await message.reply(f'Lỗi khi lấy msv: {e}')
        return

    if student_id is None:
        text = "Bạn chưa lấy dữ liệu thời khóa biểu\n"\
               "Dùng /info để biết thêm chi tiết"
        await message.answer(text)
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
    try:
        student_id = await find_student_id(message['from'].username)
    except Exception as e:
        await message.reply(f'Lỗi khi lấy msv: {e}')
        return

    if student_id is None:
        text = "Bạn chưa lấy dữ liệu thời khóa biểu\n"\
               "Dùng /info để biết thêm chi tiết"
        await message.answer(text)
        return

    try:
        testtable = await find_all_testtable(student_id)
    except Exception as e:
        await message.reply(f'Lỗi khi lấy lịch thi: {e}')
    if testtable == []:
        await message.reply('Bạn chưa lấy môn thi, /info để biết chi tiết')
        return
    else:
        title = get_subject(testtable)

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
        if testtable is None:
            await message.reply('Không có lịch thi')
            return
        else:
            text = f"<b>Thời gian:</b> {testtable['date']}".replace('\n', " ")
            info = \
                f"\n<b>Msv:</b> {testtable['student_id']}\n"\
                f"<b>Phòng thi:</b> {testtable['room']}\n"\
                f"<b>Môn thi:</b> {testtable['subject']}\n"\
                f"<b>Tiết thi:</b> {testtable['time']}\n"\
                f"<b>Giờ thi:</b> {testtable['time_start']}"
            text = text + info
            await message.reply(text)
    else:
        text = "Không có lịch thi\n"\
               "Có thể chạy /test để cập nhập các môn thi nếu đã có\n"\
               "Nếu không có môn thi có thể là chưa có lịch thi\n"\
               "Gõ /info đẻ biết thêm chi tiết cách lấy dữ liệu"
        await message.reply(text)
