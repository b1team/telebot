from aiogram import Dispatcher

from .test_command import random_answer, welcome, kb_answer, random_value


# gan command
def setup(dp: Dispatcher):
    dp.register_message_handler(welcome, commands='start')
    dp.register_message_handler(random_answer, commands='random')
    dp.register_message_handler(kb_answer)
    dp.register_callback_query_handler(
        random_value, text=["randomvalue_of10", "randomvalue_of100"])
