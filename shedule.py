from datetime import date
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database import get_text, get_word, get_users_full, get_level_stats

import logging

# базовая настройка логов
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)

async def send_daily_texts(bot):
    users = get_users_full()
    i = (date.today() - date(1970, 1, 1)).days
    current_level = 'A1'
    amount = get_level_stats(current_level)
    if amount["num_texts"]:
        text = get_text(current_level, i % amount["num_texts"])[0]
    else:
        text = None
    for level, user_id in users:
        logger.info(f"doing for user {user_id}")
        if level != current_level:
            current_level = level
            amount = get_level_stats(current_level)
            logger.info(f"now amount is {amount}")
            if amount["num_texts"]:
                text = get_text(current_level, i % amount["num_texts"])[0]
            else:
                text = None
        try:
            if text:
                await bot.send_message(user_id, text)
        except Exception as e:
            print(f"Failed to send to {user_id}: {e}")

async def send_daily_words(bot):
    users = get_users_full()
    n = (date.today() - date(1970, 1, 1)).days
    q = []
    current_level = 'A1'
    amount = get_level_stats(current_level)
    if amount["num_words"]:
        for i in range(min(amount["num_words"], 5)):
            q.append(get_word(current_level, n % amount["num_words"]))
    if len(q) > 0:
        text = f'CЛОВА ДНЯ |  Уровень {current_level}'
        for el in q:
            text += f'\n\n{el[0]} - {el[1]}\n{el[2]}'
    else:
        text = None

    for user_id, level in users:
        if level != current_level:
            current_level = level
            amount = get_level_stats(current_level)
            q.clear()
            if amount["num_words"]:
                for i in range(min(amount["num_words"], 5)):
                    q.append(get_word(current_level, n % amount["num_words"]))
            if len(q) > 0:
                text = f'CЛОВА ДНЯ |  Уровень {current_level}'
                for el in q:
                    text += f'\n\n{el[0]} - {el[1]}\n{el[2]}'
            else:
                text = None
        try:
            if len(q) > 0:
                await bot.send_message(user_id, text)
        except Exception as e:
            print(f"Failed to send to {user_id}: {e}")

async def setup_scheduler(bot):
    scheduler = AsyncIOScheduler(timezone="Europe/Minsk")
    scheduler.add_job(send_daily_texts, "cron", hour=12, minute=0, args=[bot])
    scheduler.add_job(send_daily_words, "cron", hour=15, minute=0, args=[bot])
    scheduler.start()