# ============================================================
# PROFIL HANDLERI
# ============================================================
from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == '👤 Profil')
async def profil(message: Message):
    await message.answer('Bu qisim hali tayyor emas!')
