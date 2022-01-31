from aiogram import types


async def info(message: types.Message):
    text = f"""
        <b>Chào mừng {message['from'].username} đến với chatbot</b>
    Các bạn có thể chat lung tung với bot ở đây
    Đây là project môn python
    Hãy nhắn <i>lịch thi</i>, <i>lịch học</i>, <i>thi</i>, <i>học</i> để xem các bước xem lịch của EPU
    <b>ĐẦU TIÊN, HÃY LẤY DỮ LIỆU THỜI KHÓA BIỂU</b>
    <b>Lấy thời khóa biểu theo:</b> /msv <i>188xxxxxxx</i>
    <b>SAU KHI LẤY LỊCH THÀNH CÔNG, BẠN NHẬN LỊCH THI, LỊCH HỌC theo các lệnh:</b>
    <b>Lấy lịch tuần này bằng:</b> /thisweek
    <b>Lấy lịch tuần sau bằng:</b> /nextweek
    <b>Tìm lịch học theo ngày bằng:</b> /find ngày-tháng năm
    <b>Ví dụ:</b> /find <i>20-10-2020</i>
    <b>Xem có lịch thi không bằng:</b> /test để cập nhập button môn thi
    """

    await message.answer(text)
