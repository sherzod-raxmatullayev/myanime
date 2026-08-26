# ============================================================
# ADMIN: DB BACKUP HANDLERI
# ============================================================
from datetime import datetime

from aiogram import Router, F
from aiogram.types import BufferedInputFile, Message

from ...common.constants import ADMIN_ID
from ...common.filters import IsAdmin
from .db import make_full_dump_json_bytes, zip_bytes

router = Router()


@router.message(F.text == "/sos", IsAdmin())
async def sos_backup_handler(message: Message):
    # Faqat admin ishlatsin (xohlamasang olib tashla)
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Bu buyruq faqat admin uchun.")
        return

    await message.answer("🧯 Backup tayyorlanmoqda...")

    json_bytes = await make_full_dump_json_bytes()

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    json_name = f"db_backup_{stamp}.json"
    zip_name = f"db_backup_{stamp}.zip"

    zipped = zip_bytes(json_name, json_bytes)

    # Telegramga ZIP fayl yuboramiz
    file = BufferedInputFile(zipped, filename=zip_name)

    await message.bot.send_document(
        chat_id=ADMIN_ID,
        document=file,
        caption=f"✅ DB Backup (dumpdata) | {stamp}\n📦 {zip_name}"
    )

    await message.answer("✅ Backup yuborildi.")
