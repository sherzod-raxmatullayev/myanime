# ============================================================
# STATISTIKA DB FUNKSIYASI
# ============================================================
from asgiref.sync import sync_to_async

from main.models import AppLacations, Anime, Channels, Subscriptions, TelegramUsers, Video


@sync_to_async
def db_get_stats():
    return {
        "users": TelegramUsers.objects.count(),
        "anime": Anime.objects.count(),
        "apps": AppLacations.objects.count(),
        "channels": Channels.objects.count(),
        "videos": Video.objects.count(),
        "subs": Subscriptions.objects.count(),
    }
