from aiogram import Bot, Dispatcher
from config import settings
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=settings.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
