import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
from config import TOKEN
from handlers import router
from aiogram.fsm.storage.memory import MemoryStorage
import logging


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="search", description="Поиск заказов"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

async def main():
    dp = Dispatcher(storage=MemoryStorage())
    categories = ['Все категории', 'Программирование', '3D Графика', 'Фотография', 'Дизайн и Арт', 'Обучение/консалт', 'Переводы', 'Архитектура/Интерьер', 'Маркетинг', 'Аудио/Видео', 'Менеджмент', 'Тексты', 'Сети и инфосистемы', 'Инжиниринг', 'Другое']
    dates = ["За месяц", "За неделю", "За 1 день"]

    await set_bot_commands(bot)
    dp.include_router(router)
    await dp.start_polling(bot, categories=categories, dates=dates)

if __name__ == "__main__":
    # request_data_queue = asyncio.Queue()
    asyncio.run(main())
    


