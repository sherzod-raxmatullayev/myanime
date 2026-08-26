# ============================================================
# ADMIN PANEL HANDLERLARI
# ============================================================
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ...common.filters import IsAdmin
from .buttons import admin_panel_buttons

router = Router()


@router.message(Command('panel'), IsAdmin())
async def adminpanel(message: Message):
    await message.answer('Admin panel', reply_markup=admin_panel_buttons)


@router.message(F.text == '⬅️ Orqaga', IsAdmin())
async def backirqaadmin(message: Message, state: FSMContext):
    await message.delete()
    await state.clear()
    await message.answer('Admin panel', reply_markup=admin_panel_buttons)
