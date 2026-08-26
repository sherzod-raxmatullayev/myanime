# ============================================================
# ANIME SOZLAMALARI TUGMALARI
# ============================================================
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

anime_settings_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text='➕ Anime qo‘shish'),
            KeyboardButton(text="🗑 Anime o'chirish")
        ],
        [
            KeyboardButton(text='⬅️ Orqaga')
        ]
    ]
)
