# ============================================================
# QISM (VIDEO) BOSHQARUVI DB FUNKSIYALARI
# ============================================================
from asgiref.sync import sync_to_async
from django.db.models import Max

from main.models import Anime, Subscriptions, Video


@sync_to_async
def anime_exists(anime_id: int) -> bool:
    return Anime.objects.filter(id=anime_id).exists()


@sync_to_async
def get_anime(anime_id: int) -> Anime:
    return Anime.objects.get(id=anime_id)


@sync_to_async
def get_subscribers(anime_id: int):
    return list(Subscriptions.objects.filter(anime_id=anime_id))


@sync_to_async
def create_video(anime, series_number: int, video_file_id: str) -> Video:
    return Video.objects.create(
        anime=anime,
        series_number=series_number,
        video_file_id=video_file_id
    )


@sync_to_async
def video_exists(video_id: int) -> bool:
    return Video.objects.filter(id=video_id).exists()


@sync_to_async
def delete_video(video_id: int):
    return Video.objects.filter(id=video_id).delete()


@sync_to_async
def get_next_series_number(anime_id: int) -> int:
    m = Video.objects.filter(anime_id=anime_id).aggregate(Max("series_number"))["series_number__max"]
    return (m or 0) + 1


@sync_to_async
def add_video(anime_id: int, series_number: int, file_id: str):
    return Video.objects.create(
        anime_id=anime_id,
        series_number=series_number,
        video_file_id=file_id
    )
