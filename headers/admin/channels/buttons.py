# ============================================================
# KANAL BOSHQARUVI TUGMALARI
# ============================================================
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from main.models import Channels


def admin_channels_menu_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="➕ Kanal qo'shish")
    kb.button(text="➖ Kanal o'chirish")
    kb.button(text="📋 Kanallar ro'yxati")
    kb.button(text="⬅️ Orqaga")
    kb.adjust(2, 1)
    return kb.as_markup(resize_keyboard=True)


def channels_delete_inline_kb(channels: list[Channels]):
    kb = InlineKeyboardBuilder()
    for ch in channels:
        kb.button(
            text=f"🗑 {ch.name} (id:{ch.id})",
            callback_data=f"ch_del:{ch.id}"
        )
    kb.button(text="❌ Bekor qilish", callback_data="ch_del_cancel")
    kb.adjust(1)
    return kb.as_markup()
