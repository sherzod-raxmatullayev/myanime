# ============================================================
# QIDIRUV DB FUNKSIYALARI
# ============================================================
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from asgiref.sync import sync_to_async

from main.models import Anime


@sync_to_async
def search_anime_by_name_uz(query: str, limit: int = 10):
    """Anime qidirish (uzbekcha nom bo'yicha) va inline tugmalar generatsiya qilish."""
    animes = list(
        Anime.objects.filter(name_uz__icontains=query)
        .values('id', 'name_uz')[:limit]
    )
    if not animes:
        return None

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for anime in animes:
        button = InlineKeyboardButton(
            text=anime['name_uz'],
            callback_data=f"anime_{anime['id']}"
        )
        keyboard.inline_keyboard.append([button])
    keyboard.inline_keyboard.append([InlineKeyboardButton(text='Orqaga', callback_data='back')])

    return keyboard


@sync_to_async
def search_anime_by_name_en(query: str, limit: int = 10):
    """Anime qidirish (inglizcha nom bo'yicha) va inline tugmalar generatsiya qilish."""
    animes = list(
        Anime.objects.filter(name_en__icontains=query)
        .values('id', 'name_en')[:limit]
    )
    if not animes:
        return None

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for anime in animes:
        button = InlineKeyboardButton(
            text=anime['name_en'],
            callback_data=f"anime_{anime['id']}"
        )
        keyboard.inline_keyboard.append([button])
    keyboard.inline_keyboard.append([InlineKeyboardButton(text='Orqaga', callback_data='back')])

    return keyboard
