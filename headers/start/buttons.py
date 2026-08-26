# ============================================================
# ASOSIY MENYU TUGMASI
# ============================================================
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔍 Qidirish")],                 # 1-qator
        [
            KeyboardButton(text="📺 Kuzatilayotgan"),         # 2-qator
            KeyboardButton(text="👤 Profil")
        ],
        [KeyboardButton(text="📩 Aloqa")]                     # 3-qator
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)
