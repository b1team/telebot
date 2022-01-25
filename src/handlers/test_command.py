import numpy
import random
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from random import randint
from model.train_model import train_model, bag_of_words
from model.train_model_v2 import response, classify
from model.train_model_v3 import classify, response
import pickle
import json

button1 = InlineKeyboardButton(text="👋 button1",
                               callback_data="randomvalue_of10")
button2 = InlineKeyboardButton(text="💋 button2",
                               callback_data="randomvalue_of100")
keyboard_inline = InlineKeyboardMarkup().add(button1, button2)

keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True,
                                one_time_keyboard=True).add(
                                    "👋 Hello!", "💋 Youtube", 'halo')


async def random_answer(message: types.Message):
    await message.reply("Select a range:", reply_markup=keyboard_inline)


async def welcome(message: types.Message):
    await message.reply("Hello! Im Gunther Bot, Please follow my YT channel",
                        reply_markup=keyboard1)


async def random_value(call: types.CallbackQuery):
    if call.data == "randomvalue_of10":
        await call.message.answer(randint(1, 10))
    if call.data == "randomvalue_of100":
        await call.message.answer(randint(1, 100))
    await call.answer()


async def kb_answer(message: types.Message):
    if message.text == 'Xin lịch thi':
        await message.reply("Lịch thi đây")
    elif message.text == 'Hủy':
        await message.reply("Nhớ để ý lịch thi nhá")
    else:
        tag, _ = classify(message.text)
        await message.reply(response(tag))

    # data, words, model, labels = train_model()
    # if message.text == 'Yes'.lower():
    #     await message.reply(f"Ready to crawl time sheet")
    # elif message.text == 'Help'.lower():
    #     await message.reply("Type 'Timetable' or 'thoi khoa bieu' to check the timetable")
    # else:
    #     results = model.predict([bag_of_words(message.text, words)])
    #     results_index = numpy.argmax(results)
    #     tag = labels[results_index]

    #     for tg in data["intents"]:
    #         if tg['tag'] == tag:
    #             responses = tg['responses']
    #     await message.reply(random.choice(responses))


    # elif message.text == '💋 Youtube':ýe
    #     await message.reply("https://youtube.com/gunthersuper")
    # else:
    #     await message.reply(f"Your message is: {message.text}")
