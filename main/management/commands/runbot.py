import asyncio
import logging

from django.core.management.base import BaseCommand

from loader import bot, dp
import bot_setup  # noqa: F401  (router shu yerda dp'ga ulanadi)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Telegram botni polling (long polling) rejimida ishga tushiradi"

    def handle(self, *args, **options):
        asyncio.run(self._run())

    async def _run(self):
        # Webhook ilgari o'rnatilgan bo'lishi mumkin — polling bilan
        # webhook bir vaqtda ishlamaydi, shuning uchun avval o'chiramiz.
        await bot.delete_webhook(drop_pending_updates=True)
        self.stdout.write(self.style.SUCCESS("Webhook o'chirildi. Polling boshlanmoqda..."))

        try:
            await dp.start_polling(bot)
            
        finally:
            await bot.session.close()
            self.stdout.write(self.style.SUCCESS("Bot ishga tushirishda xatolik yuz berdi."))