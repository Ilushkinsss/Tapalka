import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router

logging.basicConfig(level=logging.INFO)

TOKEN = '7582768784:AAEIP9ffLs_mw5LvpT3IQoiJ35zFL1hPOyk'

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

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

async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())