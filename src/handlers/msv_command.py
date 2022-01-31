from aiogram import types
from utils.crawl import get_data
from utils.database import (delete_testtable, insert_student, find_student_id,
                            insert_testtable, insert_timetable, update_student,
                            delete_timetable)


async def crawl_data(message: types.Message):
    try:
        msv = message.text.split(' ')[1]
    except IndexError:
        await message.reply('Bạn chưa nhập mã sinh viên')
        return

    if len(msv) != 11:
        await message.reply('''Sai định dạng sinh viên 🤔
                            /msv 188xxxxxxxx
                            Mã sinh viên phải có 11 ký tự''')
        return

    try:
        int(msv)
    except ValueError:
        await message.reply(
            'Sai định dạng sinh viên 🤔, mã sinh viên phải là số')
        return

    text = ""
    try:
        student = await find_student_id(message['from'].username)
    except Exception as e:
        await message.reply(f'Lỗi khi lấy msv: {e}')
        return

    if not student:
        try:
            await insert_student(message['from'].username, msv)
            text = text + 'Đã thêm mới mã sinh viên của bạn\n'
        except Exception as e:
            await message.reply('Lỗi khi thêm mới msv: {}'.format(e))
            return
    else:
        try:
            await update_student(message['from'].username, msv)
            text = text + 'Đã cập nhập mã sinh viên của bạn'
        except Exception as e:
            await message.reply('Lỗi khi cập nhập msv: {}'.format(e))
            return
    try:
        await delete_timetable(student)
        await delete_testtable(student)
    except Exception as e:
        await message.reply('Lỗi khi xóa dữ liệu để cappj nhập: {}'.format(e))
        return

    try:
        data = get_data(msv)

        if type(data) is dict:
            await message.reply('''Không lấy được lịch
                Kiểm tra lại mã sinh viên
                Hoặc trang web bị lỗi
                Vui lòng thử lại sau''')
        else:
            testtable, timetable = data
            if testtable != []:
                try:
                    await insert_testtable(testtable)
                except Exception as e:
                    await message.reply('Lỗi khi thêm testtable: {}'.format(e))
            else:
                text = text + '\nKhông có lịch thi môn nào'

            if timetable != []:
                try:
                    await insert_timetable(timetable)
                except Exception as e:
                    await message.reply('Lỗi khi thêm timetable: {}'.format(e))
            else:
                text = text + '\nKhông có lịch học môn nào'

            await message.reply(f'Đã lấy dữ liệu thành công{text}')
    except Exception:
        await message.reply('Lỗi khi lấy dữ liệu, chưa lấy được lịch')
