from aiogram import Router
from aiogram import F
from aiogram.types import Message

import requests
from urllib.parse import quote
from config import system_prompt

router = Router(name=__name__)
params = {"model": "openai", "temperature": 1, "system": system_prompt}

@router.message(F.text)
async def gptprompt(message : Message):
    prompt = message.text
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    url = f"https://text.pollinations.ai/{quote(prompt)}"
    response = requests.get(url, params=params)
    await message.answer(response.content)

