# ============================================================
# KUZATILAYOTGANLAR TUGMALARI
# ============================================================
from aiogram.utils.keyboard import InlineKeyboardBuilder


def sub_menu(id):
    kb = InlineKeyboardBuilder()
    kb.button(
        text='O\'chirish',
        callback_data=f'del_{id}'
    )
    kb.adjust(1)
    return kb.as_markup()
