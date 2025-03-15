from datetime import datetime
from pathlib import Path

import pandas as pd
from aiogram import types, Router, Bot
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from db import DB


router = Router()
keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text='Загрузить файл')]
    ]
)


@router.message(Command('start'))
async def send_welcome(message: types.Message):
    msg = """
Привет, я бот для добавления новых сайтов в таблицу для будущего парсинга.
Нажми на кнопку, чтобы получить инструкцию."""

    await message.reply(msg, reply_markup=keyboard)


@router.message(lambda message: message.text == 'Загрузить файл')
async def request_file(message: types.Message):
    msg = """
Чтобы добавить новые сайты просто загрузи Excel-файл с данными.
Формат должен быть следующим: title, url, xpath"""

    await message.reply(msg)


@router.message(lambda message: message.document)
async def handle_document(message: types.Message, bot: Bot, db: DB):
    if not message.document.file_name.endswith(('.xlsx', '.xls')):
        await message.reply('Пожалуйста, загрузите файл в формате Excel (.xlsx или .xls)')
        return
    
    # скачиваем и сохраняем файл в папке uploads, Pathlib для кроссплатформенности
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    filename = f'{message.from_user.full_name}  {datetime.now()}.xlsx'
    filepath = Path("uploads").joinpath(filename)
    await message.bot.download(file, destination=filepath)

    excel_data = pd.read_excel(filepath)
    
    required_columns = ['title', 'url', 'xpath']
    if not all(col in excel_data.columns for col in required_columns):
        await message.reply('Файл должен соответствовать формату: title, url, xpath')
        return

    response = 'В очередь парсера были добавлены следующие данные:\n\n'
    response += "\n".join(
        [f"{i+1})   {row['title']} \n{row['url']} \n{row['xpath']} \n" 
        for i, row in excel_data.iterrows()]
    )
    
    await message.reply(response)
    await db.insert_new_sites(excel_data)