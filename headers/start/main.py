# ============================================================
# START / ASOSIY MENYU
# ============================================================
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from asgiref.sync import sync_to_async

from main.models import TelegramUsers

from ..anime.db import send_anime_by_id
from ..common.constants import DEVLOPER_ID
from ..common.texts import WELCOME_TEXT
from .buttons import main_menu

router = Router()


@router.callback_query(F.data == 'start')
async def handle_start_callback(message: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        user, created = await sync_to_async(lambda: TelegramUsers.objects.get_or_create(
            telegram_id=message.from_user.id
        ))()
        if created:
            text_new_user = (
                f"Yangi foydalanuvchi qo'shildi\n\n"
                f"ID: {message.from_user.id}\n"
                f"Full name: {message.from_user.first_name}\n"
            )
            await message.bot.send_message(chat_id=DEVLOPER_ID, text=text_new_user)
        await message.message.delete()
        await message.message.answer(WELCOME_TEXT, reply_markup=main_menu)
    except Exception as e:
        print('inline startda xato', e)
        await message.message.answer(WELCOME_TEXT, reply_markup=main_menu)


@router.message(CommandStart())
async def handle_start_command(message: Message, state: FSMContext):
    try:
        await state.clear()
        if len(message.text.split(' ')) == 2:
            anime_id = message.text.split(' ')[1]
            await send_anime_by_id(message=message, anime_id=int(anime_id))

        user, created = await sync_to_async(lambda: TelegramUsers.objects.get_or_create(
            telegram_id=message.from_user.id
        ))()
        if created:
            text_new_user = (
                "━━━━━━━━━━━━━━\n"
                "🆕 *Yangi foydalanuvchi*\n"
                "━━━━━━━━━━━━━━\n\n"
                f"🆔 ID: `{message.from_user.id}`\n"
                f"👤 To‘liq ism: {message.from_user.first_name}"
            )
            await message.bot.send_message(chat_id=DEVLOPER_ID, text=text_new_user, parse_mode='Markdown')

        await message.answer(WELCOME_TEXT, reply_markup=main_menu)
    except Exception as e:
        print('inline startda xato', e)
        await message.answer("Asosiy sahifa!", reply_markup=main_menu)


@router.callback_query(F.data == 'back')
async def closes(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.delete()
    await call.message.answer(WELCOME_TEXT, reply_markup=main_menu)
