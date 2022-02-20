from aiogram import types
from utils.database import find_one_timetable, find_student_id
from utils.supports import validate, check_date_format


async def find_by_day(message: types.Message):
    # split the message and get date at the second split and try except
    # try except validate the second split is not true reply error message
    # find_student_id by username from message['from], if student_id is None reply dont have student_id and return
    # find_one_timetable by student_id and date, find_one_timetable is return a list of dict
    # use for to loop timetable and reply message
    # if timetable is empty, reply message is empty
    # else reply message is contain list of dict with format {'subject': '', 'time': '', 'room': ''}
    # if message is None reply error message
    try:
        date = message.text.split(' ')[1]
    except IndexError:
        await message.reply('Bạn chưa nhập ngày')
        return
    if check_date_format(date) is False or validate(date) is False:
        text = "Bạn nhập sai ngày tháng năm\n"\
               "Vui lòng nhập lại, theo định dạng dd-mm-yyyy\n"\
               "Ví dụ: /find 01-03-2022"
        await message.reply(text)
        return

    try:
        student_id = await find_student_id(message['from'].username)
    except Exception as e:
        await message.reply(f'Lỗi khi lấy msv: {e}')
        return

    if student_id is None:
        text = "Bạn chưa lấy dữ liệu thời khóa biểu\n"\
                "Dùng /info để biết thêm chi tiết"
        await message.reply(text)
        return
    else:
        try:
            timetable = await find_one_timetable(date, student_id)
        except Exception as e:
            await message.reply(f'Lỗi khi lấy thời khóa biểu: {e}')
            return
        if timetable == []:
            await message.reply(f'Không tìm thấy lịch học ngày {date}')
            return
        else:
            text = ''
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
                text = text + info
            await message.reply(text)
