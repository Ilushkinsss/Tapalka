import logging
import aiohttp
from aiogram import types

logging.basicConfig(level=logging.INFO)

API_URL = 'http://localhost:8000' #

async def send_welcome(message: types.Message):
    await message.reply("Привет!")

async def send_help(message: types.Message):
    help_text = (
        "/start - Начать взаимодействие с ботом\n"
        "/help - Получить помощь\n"
        "/get_data - Получить данные из API\n"
        "/send_data - Отправить данные в API"
    )
    await message.reply(help_text)

async def get_data(message: types.Message):
    async with aiohttp.ClientSession() as session:
    try:
        async with session.get(f'{API_URL}/data') as response:
            if response.status == 200:
                data = await response.json()
                await message.reply(f"Полученные данные: {data}")
            else:
                await message.reply("Не удалось получить данные.")
    except aiohttp.ClientError as e:
        await message.reply(f"Ошибка подключения к API: {e}")


async def send_data(message: types.Message):
    data_to_send = {"key": "value"}
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{API_URL}/data', json=data_to_send) as response:
            if response.status == 201:
                await message.reply("Данные успешно отправлены.")
            else:
                await message.reply("Не удалось отправить данные.")