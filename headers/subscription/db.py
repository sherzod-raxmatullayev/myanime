# ============================================================
# OBUNA (MAJBURIY KANAL) DB FUNKSIYALARI
# ============================================================
from asgiref.sync import sync_to_async

from main.models import Channels


async def get_all_channels() -> list:
    return await sync_to_async(lambda: list(Channels.objects.all()))()
