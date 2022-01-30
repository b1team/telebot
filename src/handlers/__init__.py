from aiogram import Dispatcher

from .answer import random_answer, welcome, kb_answer, random_value
from utils.supports import get_all_dates_of_week


# gan command
def setup(dp: Dispatcher):
    dp.register_message_handler(welcome, commands='start')
    dp.register_message_handler(random_answer, commands='random')
    dp.register_message_handler(kb_answer)
    dp.register_callback_query_handler(
        random_value, text=[i for _, i in get_all_dates_of_week()])
