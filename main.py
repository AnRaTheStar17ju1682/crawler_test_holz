import asyncio
import os
import logging

from aiogram import Bot, Dispatcher

from db import DB
from bot import router


# я знаю, что это должно загружаться из .env файла, но в тестовом задании это принесет только неудобства
API_TOKEN = ''


async def main():
    # это папка для хранения эксель файлов
    os.makedirs('uploads', exist_ok=True)
    db = DB('sites.db')
    await db.init_db()
    
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    await dp.start_polling(bot, db=db)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())