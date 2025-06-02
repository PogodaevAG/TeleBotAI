import asyncio
from config import TOKEN

from aiogram import Bot, Dispatcher

from app.db import create_table
from app.handlers import router


async def main():
    # Объект бота
    bot = Bot(token=TOKEN)
    # Диспетчер
    dp = Dispatcher()
    dp.include_router(router)
    # Запускаем создание таблицы базы данных
    await create_table()
    # Запуск процесса поллинга новых апдейтов
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')