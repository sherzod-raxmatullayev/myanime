# ============================================================
# UMUMIY (bir nechta bo'limda ishlatiladigan) TUGMALAR
# ============================================================
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def backk():
    kb = InlineKeyboardBuilder()
    kb.button(text='Orqaga', callback_data='back')
    return kb.adjust(1).as_markup()


def cancel_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="❌ Bekor qilish")
    return kb.as_markup(resize_keyboard=True)
