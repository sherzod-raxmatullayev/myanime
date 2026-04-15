from tkinter import E

from loader import dp, bot
import asyncio
import logging



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from headers import router


dp.include_router(router)

async def main():
    await dp.start_polling(bot)

    

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print("Bot to‘xtatildi ✅")
        logger.error(f"Botda xatolik yuz berdi: {e}")