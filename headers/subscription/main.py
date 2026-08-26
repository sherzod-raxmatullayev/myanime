# ============================================================
# MAJBURIY OBUNA HANDLERLARI
# ============================================================
from aiogram import Router, F
from aiogram.types import CallbackQuery, ChatJoinRequest, Message
from asgiref.sync import sync_to_async

from main.models import AppLacations

from .buttons import build_subscription_keyboard
from .filters import call_data, mess_data

router = Router()


@router.message(mess_data())
async def mandatory_message(message: Message):
    referel = None
    if message.text.startswith('/start'):
        full_args = message.text.split(' ')
        if len(full_args) > 1:
            _, referel = full_args
    kb = await build_subscription_keyboard(message.from_user.id, referel)
    if kb:
        await message.answer("Iltimos, quyidagi kanallarga obuna bo'ling va tekshirishni  bosing:", reply_markup=kb.as_markup())


@router.callback_query(call_data())
async def mandatory_callback(query: CallbackQuery):
    kb = await build_subscription_keyboard(query.from_user.id, None)
    if kb:
        await query.answer("Iltimos, quyidagi kanallarga obuna bo'ling va /start bosing.", reply_markup=kb.as_markup())


@router.chat_join_request(F.chat.type.in_({"supergroup", "channel"}))
async def handle_join_request(event: ChatJoinRequest):
    await sync_to_async(lambda: AppLacations.objects.create(user=event.from_user.id, channel=event.chat.id))()
