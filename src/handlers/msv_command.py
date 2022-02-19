from aiogram import types
from utils.crawl import get_data
from utils.database import (delete_testtable, insert_student, find_student_id,
                            insert_testtable, insert_timetable, update_student,
                            delete_timetable)


async def crawl_data(message: types.Message):
    try:
        msv = message.text.split(' ')[1]
        await message.answer('Lấy thành công MSV: {}'.format(msv))
    except IndexError:
        await message.reply('Bạn chưa nhập mã sinh viên')
        return

    if len(msv) != 11:
        text = "Sai định dạng sinh viên 🤔\n"\
               "Lấy dữ liệu theo /msv 188xxxxxxxx\n"\
               "Mã sinh viên phải có 11 ký tự"
        await message.reply(text)
        return

    try:
        int(msv)
    except ValueError:
        await message.reply(
            'Sai định dạng sinh viên 🤔, mã sinh viên phải là số')
        return
    await message.answer('Kiểm tra mã sinh viên đạt chuẩn')

    text = ""
    try:
        student = await find_student_id(message['from'].username)
    except Exception as e:
        await message.reply(f'Lỗi khi lấy msv: {e}')
        return

    if not student:
        try:
            await insert_student(message['from'].username, msv)
            await message.answer('Đã lưu mã sinh viên')
        except Exception as e:
            await message.answer('Lỗi khi thêm mới msv: {}'.format(e))
            return
    else:
        try:
            await update_student(message['from'].username, msv)
            await message.answer('Đã cập nhật mã sinh viên')
        except Exception as e:
            await message.answer('Lỗi khi cập nhập msv: {}'.format(e))
            return
    try:
        await delete_timetable(student)
        await delete_testtable(student)
        await message.answer("Đã làm sạch thời khóa biểu cũ")
    except Exception as e:
        await message.reply('Lỗi khi xóa dữ liệu để cập nhập: {}'.format(e))
        return

    try:
        await message.answer("Đang lấy dữ liệu...")
        data = get_data(msv)
        if type(data) is dict:
            text = "Không lấy được lịch\n"\
                   "Kiểm tra lại mã sinh viên\n"\
                   "Hoặc trang web bị lỗi\n"\
                   "Vui lòng thử lại sau"
            await message.reply(text)
            return
        else:
            await message.answer("Đã lấy dữ liệu thành công")
            testtable, timetable = data
            if testtable != []:
                try:
                    await insert_testtable(testtable)
                    await message.answer("Lưu thành công lịch thi")
                except Exception as e:
                    await message.reply('Lỗi khi thêm testtable: {}'.format(e))
            else:
                await message.answer('Không có lịch thi môn nào')

            if timetable != []:
                try:
                    await insert_timetable(timetable)
                    await message.answer("Lưu thành công lịch học")
                except Exception as e:
                    await message.reply('Lỗi khi thêm timetable: {}'.format(e))
            else:
                await message.answer('Không có lịch học môn nào')

            await message.reply(
                f'Đã cập nhật thành công lịch học và thi cho {message["from"].username} với mã sinh viên {msv}'
            )
            await message.answer('Xem các lịch học và thi của bạn: /info')
    except Exception:
        await message.reply('Lỗi khi lấy dữ liệu, chưa lấy được lịch')
