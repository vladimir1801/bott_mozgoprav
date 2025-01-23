import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from openai import OpenAI
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Настройка OpenAI API
client = OpenAI(api_key=OPENAI_API_KEY)

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Обработка команды /start
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Я бот, использующий OpenAI. Напиши мне что-нибудь, и я постараюсь ответить.")

# Обработка текстовых сообщений
@dp.message()
async def handle_message(message: Message):
    try:
        print(f"Получено сообщение: {message.text}")

        # Новый способ вызова OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — помощник."},
                {"role": "user", "content": message.text}
            ]
        )

        # Извлечение текста ответа
        reply = response.choices[0].message.content
        await message.answer(reply)
    except Exception as e:
        print(f"Ошибка: {e}")
        await message.answer("Произошла ошибка. Попробуйте позже.")

# Запуск бота
async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

