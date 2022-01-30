from aiogram import Bot, Dispatcher, types
from config import settings
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=settings.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
