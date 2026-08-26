# ============================================================
# KUZATILAYOTGANLAR DB FUNKSIYALARI
# ============================================================
from asgiref.sync import sync_to_async

from main.models import Subscriptions


async def get_user_subscriptions(user_id: int):
    return await sync_to_async(list)(
        Subscriptions.objects.filter(telegram_user_id=user_id).select_related('anime')
    )


async def delete_subscription(sub_id, user_id: int) -> int:
    deleted, _ = await sync_to_async(
        Subscriptions.objects.filter(
            id=sub_id,
            telegram_user_id=user_id,
        ).delete
    )()
    return deleted
