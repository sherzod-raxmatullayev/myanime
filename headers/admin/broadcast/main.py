# ============================================================
# ADMIN: XABAR TARQATISH HANDLERLARI
# ============================================================
import asyncio

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from asgiref.sync import sync_to_async

from main.models import TelegramUsers

from ...common.buttons import backk
from ...common.filters import IsAdmin
from ..panel.buttons import admin_panel_buttons
from .states import messagesClass

router = Router()


@router.message(F.text == "📨 Xabar tarqatish", IsAdmin())
async def tarqart(message: Message, state: FSMContext):
    await message.answer(text="Tarqatmoqchi bo'lgan xabaringizni yuboring.", reply_markup=backk())
    await state.set_state(messagesClass.mess)


@router.message(messagesClass.mess, IsAdmin())
async def message_state(message: Message, state: FSMContext):
    users = await sync_to_async(lambda: list(TelegramUsers.objects.all()))()

    error = 0
    count = 0

    for user in users:
        try:
            if message.text:
                await message.bot.send_message(
                    chat_id=user.telegram_id,
                    text=message.text
                )
            elif message.photo:
                await message.bot.send_photo(
                    chat_id=user.telegram_id,
                    photo=message.photo[-1].file_id,
                    caption=message.caption if message.caption else None
                )
            elif message.video:
                await message.bot.send_video(
                    chat_id=user.telegram_id,
                    video=message.video.file_id,
                    caption=message.caption if message.caption else None
                )

            count += 1
            await asyncio.sleep(0.1)

        except Exception as e:
            print('Xabar tarqatishda muamo:', e)
            error += 1

    await message.answer(
        text=f"✅ Xabar yetkazildi: {count}\n❌ Tarqatilmadi: {error}",
        reply_markup=admin_panel_buttons
    )
    await state.clear()
