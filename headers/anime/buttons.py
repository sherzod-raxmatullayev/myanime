# ============================================================
# ANIME KO'RISH / YUKLASH TUGMALARI
# ============================================================
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def build_download_button(anime_id: int) -> InlineKeyboardMarkup:
    """Kanaldagi post ostiga qo'yiladigan yagona 'Yuklash' tugmasi (deep-link orqali)."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='⬇️ Yuklash',
                    url=f'https://t.me/FOX_TV_STUDIOS_ROBOT?start={anime_id}'
                )
            ]
        ]
    )


def build_anime_view_keyboard(anime_id) -> InlineKeyboardMarkup:
    """Anime kartochkasi ostidagi 'Kuzatish' + 'Yuklash' tugmalari."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='⭐ Kuzatish', callback_data=f'follow_{anime_id}'),
                InlineKeyboardButton(text='⬇️ Yuklash', callback_data=f'down_{anime_id}_1'),
            ]
        ]
    )


def build_series_download_keyboard(anime_id) -> InlineKeyboardMarkup:
    """Yangi qism obunachilarga yuborilganda ko'rsatiladigan yagona 'Yuklash' tugmasi."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='⬇️ Yuklash', callback_data=f'down_{anime_id}_1')]
        ]
    )
