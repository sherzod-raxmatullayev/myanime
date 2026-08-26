# ============================================================
# ANIME QO'SHISH/O'CHIRISH DB FUNKSIYALARI
# ============================================================
from asgiref.sync import sync_to_async

from main.models import Anime


@sync_to_async
def create_anime(data: dict) -> Anime:
    return Anime.objects.create(
        name_uz=data['name_uz'],
        name_en=data['name_en'],
        discreptin=data['discreptin'],
        janr=data['janr'],
        year=data['year'],
        series_count=data['series_count'],
        photo_id=data['photo_id']
    )


@sync_to_async
def anime_exists(anime_id: int) -> bool:
    return Anime.objects.filter(id=anime_id).exists()


@sync_to_async
def delete_anime(anime_id: int):
    return Anime.objects.filter(id=anime_id).delete()
