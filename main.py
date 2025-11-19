import asyncio
import logging
from aiogram import Bot, Dispatcher

import database
from routers import router as main_router
from config import token

dp = Dispatcher()
dp.include_router(main_router)
bot = Bot(token=token)

async def main():
    database.create_tables()
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

asyncio.run(main())