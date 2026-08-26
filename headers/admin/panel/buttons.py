# ============================================================
# ADMIN PANEL TUGMALARI
# ============================================================
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

admin_panel_buttons = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text='🎬 Anime sozlamalari'),
            KeyboardButton(text='🧩 Qism sozlamalari')
        ],
        [
            KeyboardButton(text='📢 Kanal sozlamalari'),
            KeyboardButton(text='📨 Xabar tarqatish')
        ],
        [
            KeyboardButton(text='📊 Statistika'),
            KeyboardButton(text='👥 Foydalanuvchini boshqarish')
        ]
    ]
)
