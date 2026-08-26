# ============================================================
# MAJBURIY OBUNA FILTERLARI
# ============================================================
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from asgiref.sync import sync_to_async

from main.models import AppLacations

from .db import get_all_channels


async def has_pending_channel(event) -> bool:
    """
    Foydalanuvchi hali barcha majburiy kanallarga a'zo bo'lmagan
    (yoki AppLacations'da yozuvi bo'lmagan) bo'lsa True qaytaradi.
    `event` CallbackQuery yoki Message bo'lishi mumkin — ikkalasida ham
    .from_user va .bot mavjud.
    """
    user_id = event.from_user.id

    channels = await get_all_channels()
    if not channels:
        return False

    for channel in channels:
        channel_id = channel.telegram_id

        try:
            member = await event.bot.get_chat_member(channel_id, user_id)
            apl_exists = await sync_to_async(lambda: AppLacations.objects.filter(
                user=user_id, channel=channel_id
            ).exists())()

            if member.status in ("creator", "administrator", "member", "restricted") or apl_exists:
                continue
            else:
                return True

        except Exception as e:
            # Tekshiruv ishlamasa, foydalanuvchini majburiy obunadan o‘tkazib yubormaymiz.
            print(f'Kanal obunasini tekshirishda xato ({channel_id}):', e)
            return True

    return False


class call_data(BaseFilter):
    async def __call__(self, call: CallbackQuery) -> bool:
        return await has_pending_channel(call)


class mess_data(BaseFilter):
    async def __call__(self, call: Message) -> bool:
        return await has_pending_channel(call)
