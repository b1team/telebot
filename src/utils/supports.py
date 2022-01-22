from datetime import datetime


def get_date_test(date: str):
    date_str = date[date.find('\n') + 2:].replace(')', '')
    date_object = datetime.strptime(date_str, '%d-%m-%Y').date()

    return date_object


# tìm giờ bắt đầu học
def get_time_start(tiet: str):
    i = tiet[:2].strip()
    dict_time = {
        "1": "7:00",
        "2": "7:55",
        "3": "8:50",
        "4": "9:50",
        "5": "10:45",
        "6": "12:30",
        "7": "13:25",
        "8": "14:20",
        "9": "15:20",
        "10": "16:15",
        "11": "17:30",
        "12": "18:25",
        "13": "19:20",
        "14": "20:15"
    }

    return dict_time[i]


# tìm ngày lịch học
def get_date(date_string: str):
    date_str = date_string[3:13]
    date_object = datetime.strptime(date_str, '%d-%m-%Y').date()

    return date_object


# format ngay thang nam
def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d-%m-%Y')
    except ValueError:
        raise ValueError("Incorrect data format, should be DD-MM-YYY")

    return True
