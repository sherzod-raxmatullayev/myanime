# ============================================================
# ADMIN: STATISTIKA HANDLERI
# ============================================================
from aiogram import Router, F
from aiogram.types import Message

from ...common.filters import IsAdmin
from ..panel.buttons import admin_panel_buttons
from .db import db_get_stats

router = Router()


@router.message(F.text == "📊 Statistika", IsAdmin())
async def show_stats(message: Message):
    s = await db_get_stats()
    text = (
        "📊 *Statistika:*\n\n"
        f"👤 TelegramUsers: *{s['users']}*\n"
        f"🎬 Anime: *{s['anime']}*\n"
        f"📱 AppLacations: *{s['apps']}*\n"
        f"📢 Channels: *{s['channels']}*\n"
        f"🎞 Video: *{s['videos']}*\n"
        f"⭐ Subscriptions: *{s['subs']}*\n"
    )
    await message.answer(text, parse_mode="Markdown", reply_markup=admin_panel_buttons)
