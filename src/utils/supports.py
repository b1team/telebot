from datetime import datetime, timedelta, date


def get_date_test(date: str):
    date_str = date[date.find('\n') + 2:].replace(')', '')
    date_object = datetime.strptime(date_str, '%d-%m-%Y').date()

    return date_object


def get_str_date_test(date: str):
    date_str = date[date.find('\n') + 2:].replace(')', '')

    return date_str


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
    # date_object = datetime.strptime(date_str, '%d-%m-%Y').date()

    return date_str


# format ngay thang nam
def validate(date_text):
    try:
        datetime.strptime(date_text, '%d-%m-%Y')
    except ValueError:
        return False

    return True


# get all dates of week
def get_all_dates_of_week(days=0):
    labels = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ nhật']
    theday = date.today() + timedelta(days=days)
    weekday = theday.isoweekday()
    start = theday - timedelta(days=weekday)
    dates = [start + timedelta(days=d) for d in range(1, 8)]
    dates = [str(d.strftime("%d-%m-%Y")) for d in dates]

    dates = list(zip(labels, dates))

    return dates
