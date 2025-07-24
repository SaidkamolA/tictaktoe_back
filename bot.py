import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import asyncio

# Впиши сюда свой токен бота
TOKEN = "8201827836:AAHQoG6Acgoxycmz7YT55giCAARqCnuHt7k"

# URL мини-приложения (замени на актуальный, например, http://localhost:8000 или продакшн-URL)
WEBAPP_URL = "http://localhost:8000"  # или другой URL, где будет фронтенд

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    kb = ReplyKeyboardBuilder()
    kb.add(
        KeyboardButton(
            text="Играть",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    )
    await message.answer(
        "Привет! Нажми 'Играть', чтобы начать игру в крестики-нолики.",
        reply_markup=kb.as_markup(resize_keyboard=True)
    )

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 