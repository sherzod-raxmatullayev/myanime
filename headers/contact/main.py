# ============================================================
# ALOQA HANDLERI
# ============================================================
from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == '📩 Aloqa')
async def aloqa(message: Message):
    await message.answer('Aloqa uchun admin: @sherzod_raxmatullayev')
