from aiogram import Dispatcher

from .answer import random_answer, welcome, kb_answer, random_value
from .find_command import find_by_day
from .info_command import info
from .msv_command import crawl_data
from .next_week_command import next_week, next_week_dates
from .this_week_command import this_week_dates, this_week
from .test_command import get_markup, show_testtable
from utils.supports import get_all_dates_of_week


# gan command
def setup(dp: Dispatcher):
    dp.register_message_handler(welcome, commands='start')

    dp.register_message_handler(random_answer, commands='random')
    dp.register_callback_query_handler(
        random_value, text=[i for _, i in get_all_dates_of_week()])

    dp.register_message_handler(find_by_day, commands='find')
    dp.register_message_handler(info, commands='info')
    dp.register_message_handler(crawl_data, commands='msv')

    dp.register_message_handler(next_week_dates, commands='nextweek')
    dp.register_callback_query_handler(
        next_week, text=[i for _, i in get_all_dates_of_week(7)])

    dp.register_message_handler(this_week_dates, commands='thisweek')
    dp.register_callback_query_handler(
        this_week, text=[i for _, i in get_all_dates_of_week()])

    dp.register_message_handler(get_markup, commands='test')
    dp.register_message_handler(show_testtable)
    dp.register_message_handler(kb_answer)
