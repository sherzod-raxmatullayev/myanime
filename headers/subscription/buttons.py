# ============================================================
# MAJBURIY OBUNA TUGMALARI
# ============================================================
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from asgiref.sync import sync_to_async

from loader import bot
from main.models import AppLacations

from .db import get_all_channels


async def build_subscription_keyboard(user_id: int, referal) -> InlineKeyboardMarkup | None:
    """Foydalanuvchi hali a'zo bo'lmagan kanallar ro'yxatini + 'Tekshirish' tugmasini quradi."""
    kb = InlineKeyboardBuilder()

    channels = await get_all_channels()
    if not channels:
        return None

    for channel in channels:
        channel_id = channel.telegram_id
        try:
            member = await bot.get_chat_member(channel_id, user_id)
            apl_exists = await sync_to_async(lambda: AppLacations.objects.filter(
                user=user_id, channel=channel_id
            ).exists())()

            if member.status in ("creator", "administrator", "member", "restricted") or apl_exists:
                continue
            else:
                kb.button(text=channel.name, url=channel.link)

        except Exception:
            kb.button(text=channel.name, url=channel.link)

    if referal != None:
        kb.button(text='✅ Tekshirish', callback_data=f'tekshir_{referal}')
    else:
        kb.button(text='✅ Tekshirish', callback_data='start')

    if kb:
        return kb.adjust(1)
