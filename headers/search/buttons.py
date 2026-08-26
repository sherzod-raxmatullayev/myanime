# ============================================================
# QIDIRUV TUGMALARI
# ============================================================
from aiogram.utils.keyboard import InlineKeyboardBuilder


def search_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text='🔍 Uzbekcha nomi bilan qidirish', callback_data='search_name_uz')
    # kb.button(text='🔍 Inglizcha nomi bilan qidirish', callback_data='search_name_en')
    kb.button(text='🔍 Kodi bilan qidirish', callback_data='search_kod')
    # kb.button(text='🔍 Janri bilan qidirish', callback_data='search_janr')
    kb.button(text='Orqaga', callback_data='back')
    return kb.adjust(1).as_markup()
