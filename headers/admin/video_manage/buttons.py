# ============================================================
# QISM SOZLAMALARI TUGMALARI
# ============================================================
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

qisim_settings_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="➕ Video qo'shish"),
            KeyboardButton(text="🗑 Video o'chirish")
        ],
        [
            KeyboardButton(text='⬅️ Orqaga')
        ]
    ]
)
