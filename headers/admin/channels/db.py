# ============================================================
# KANAL BOSHQARUVI DB FUNKSIYALARI
# ============================================================
from asgiref.sync import sync_to_async

from main.models import Channels


@sync_to_async
def db_channel_create(name: str, telegram_id: int, link: str) -> Channels:
    return Channels.objects.create(name=name, telegram_id=telegram_id, link=link)


@sync_to_async
def db_channel_list():
    return list(Channels.objects.all().order_by("id"))


@sync_to_async
def db_channel_delete_by_id(pk: int) -> int:
    deleted, _ = Channels.objects.filter(id=pk).delete()
    return deleted


@sync_to_async
def db_channel_exists_by_tg_id(tg_id: int) -> bool:
    return Channels.objects.filter(telegram_id=tg_id).exists()
