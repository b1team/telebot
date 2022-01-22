import asyncio
from datetime import datetime

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


# insert thoi khoa bieu
async def insert_timetable(timetable: list):
    db = await connect_database()
    timetable = timetable

    if len(timetable) == 0:
        return True

    try:
        await db.timetable.insert_many(timetable)
    except Exception:
        raise Exception('Could not insert timetable')

    return True


# insert lich thi
async def insert_testtable(testtable: list):
    db = await connect_database()
    testtable = testtable

    if len(testtable) == 0:
        return True

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

    return document['student_id']


# tim lich hoc trong 1 ngay
async def find_timetable(date: datetime, student_id: str):
    db = await connect_database()

    try:
        document = await db.timetable.find({
            'student_id': student_id,
            'date_start': date
        })
    except Exception:
        raise Exception('Could not find a timeline')

    return document


# tim lich thi
async def find_one_testtable(subject: str, student_id: str):
    db = await connect_database()

    try:
        document = await db.testtable.find_one({
            'student_id': student_id,
            'subject': subject
        })
    except Exception:
        raise Exception('Could not find a timeline')

    return document


# tim tat ca lich thi
# lay ngay tu day roi dung cho find_one_testtable
async def find_all_testtable(student_id: str):
    db = await connect_database()

    try:
        document = await db.testtable.find({'student_id': student_id})
    except Exception:
        raise Exception('Could not find a timeline')

    return document


# cach chay
loop = asyncio.get_event_loop()
loop.run_until_complete(connect_database())
