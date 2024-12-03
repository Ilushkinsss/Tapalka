import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram.utils import executor
from config import API_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

router = Router()

@router.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("Привет!")

@router.message(Command("help"))
async def send_help(message: types.Message):
    await message.answer("Команды:\n/start - Приветствие\n/help - Помощь")

@router.message(Command("get_data"))
async def get_data(message: types.Message):
    await message.answer("Данные получены!")

@router.message(Command("send_data"))
async def send_data(message: types.Message):
    await message.answer("Данные отправлены!")

dp.include_router(router)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
