from aiogram import types


async def info(message: types.Message):
    text = """
    Chào mừng đến với chatbot
    Các bạn có thể chat lung tung với bot ở đây
    Đây là project môn python
    Hãy nhắn `lịch thi`, `lịch học`, `thi`, `học` để xem các bước xem lịch cưa EPU
    ĐẦU TIÊN, HÃY LẤY DỮ LIỆU THỜI KHÓA BIỂU
    /msv <Mã sinh viên> đây là lệnh để lấy lịch
    `vd: /msv 188xxxxxxx`
    SAU KHI LẤY LỊCH THÀNH CÔNG, BẠN NHẬN LỊCH THI, LỊCH HỌC theo các lệnh:
    /thisweek đây là lệnh lấy lịch tuần này
    /nextweek đây là lệnh lấy lịch tuần sau
    /find <ngày-tháng năm> đây là lệnh tìm kiếm lịch học
    `vd: /find 20/10/2020`
    /test để xem lịch thi
    """
    await message.reply(text)
