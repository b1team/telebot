# import asyncio

import motor.motor_asyncio
from src.config import settings


async def connect_database():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        settings.DB_URL, serverSelectionTimeoutMS=5000)
    try:
        await client.server_info()
        print('connect database successful')
    except Exception:
        raise Exception("Could not connect to server")

    return client['telebot']


# insert username tele + ma sinh vien vao 1 bang
async def insert_student(username: str, student_id: str):
    db = await connect_database()
    student = {'username': username, 'student_id': student_id}

    try:
        await db.students.insert_one(student)
    except Exception:
        raise Exception('Could not insert student')

    return True


async def update_student(username: str, student_id: str):
    db = await connect_database()

    try:
        await db.students.update_one({'username': username},
                                     {'$set': {
                                         'student_id': student_id
                                     }})
    except Exception:
        raise Exception('Could not update student')

    return True


# insert thoi khoa bieu
async def insert_timetable(timetable: list):
    db = await connect_database()

    try:
        await db.timetable.insert_many(timetable)
    except Exception:
        raise Exception('Could not insert timetable')

    return True


# insert lich thi
async def insert_testtable(testtable: list):
    db = await connect_database()

    try:
        await db.testtable.insert_many(testtable)
    except Exception:
        raise Exception('Could not insert testtable')

    return True


# tim ma sinh vien theo ten tren telegram
async def find_student_id(username: str):
    db = await connect_database()

    try:
        document = await db.students.find_one({'username': username})
    except Exception:
        raise Exception('Could not find student')
    if document is None:
        return None

    return document['student_id']


# tim lich hoc trong 1 ngay
async def find_one_timetable(date: str, student_id: str):
    db = await connect_database()
    docs = []
    try:
        document = db.timetable.find({
            'student_id': student_id,
            'date_start': date
        })
    except Exception:
        raise Exception('Could not find a time table')
    async for doc in document:
        docs.append(doc)

    return docs


# tim lich thi
async def find_one_testtable(subject: str, student_id: str):
    db = await connect_database()

    try:
        document = await db.testtable.find_one({
            'student_id': student_id,
            'subject': subject
        })
    except Exception:
        raise Exception('Could not find a timeline testtable')

    if document is None:
        return None

    return document


# tim tat ca lich thi
# lay ngay tu day roi dung cho find_one_testtable
async def find_all_testtable(student_id: str):
    db = await connect_database()
    docs = []
    try:
        document = db.testtable.find({'student_id': student_id})
    except Exception:
        raise Exception('Could not find a testtable')

    async for doc in document:
        docs.append(doc)

    return docs


async def find_all_timetable(student_id: str):
    db = await connect_database()
    docs = []
    try:
        document = db.timetable.find({'student_id': student_id})
    except Exception:
        raise Exception('Could not find a time table')

    async for doc in document:
        docs.append(doc)

    return docs


# delete many timetable by student_id
async def delete_timetable(student_id: str):
    db = await connect_database()

    try:
        await db.timetable.delete_many({'student_id': student_id})
    except Exception:
        raise Exception('Could not delete timetable')

    return True


# delete many testtables by student_id
async def delete_testtable(student_id: str):
    db = await connect_database()

    try:
        await db.testtable.delete_many({'student_id': student_id})
    except Exception:
        raise Exception('Could not delete testtable')

    return True


ls = [{
    'classname': '0101003881\n- D13CNPM4',
    'date': 'Thứ 4\n(23-02-2022)',
    'date_start': '23-02-2022',
    'room': 'C1A312',
    'student_id': '18810310361',
    'subject': 'Ngôn ngữ lập trình python',
    'time': '3 -> 5',
    'time_start': '8:50'
}, {
    'classname': '0101001816\n- D13CNPM4',
    'date': 'Thứ 6\n(18-02-2022)',
    'date_start': '18-02-2022',
    'room': 'C1A308',
    'student_id': '18810310361',
    'subject': 'Ngôn ngữ kịch bản',
    'time': '14 -> 15',
    'time_start': '20:15'
}, {
    'classname': '0101000844\n- D13CNPM4',
    'date': 'Thứ 4\n(16-02-2022)',
    'date_start': '16-02-2022',
    'room': 'C1A301',
    'student_id': '18810310361',
    'subject': 'Hệ chuyên gia',
    'time': '11 -> 12',
    'time_start': '17:30'
}, {
    'classname': '0101001132\n- D13CNPM4',
    'date': 'Thứ 3\n(25-01-2022)',
    'date_start': '25-01-2022',
    'room': 'C1A203',
    'student_id': '18810310361',
    'subject': 'Kiểm thử và đảm bảo chất lượng PM',
    'time': '13 -> 15',
    'time_start': '19:20'
}]

# cach chay
# loop = asyncio.get_event_loop()
# loop.run_until_complete(find_all_testtable('18810310361'))
