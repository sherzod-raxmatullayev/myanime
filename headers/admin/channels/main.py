# ============================================================
# ADMIN: KANAL BOSHQARUVI HANDLERLARI
# ============================================================
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from ...common.buttons import cancel_kb
from ...common.filters import IsAdmin, IsAdminCallback
from .buttons import admin_channels_menu_kb, channels_delete_inline_kb
from .db import (
    db_channel_create,
    db_channel_delete_by_id,
    db_channel_exists_by_tg_id,
    db_channel_list,
)
from .states import ChannelStates

router = Router()


@router.message(F.text == '📢 Kanal sozlamalari', IsAdmin())
async def channels_admin_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("📌 Kanal boshqaruvi:", reply_markup=admin_channels_menu_kb())


@router.message(F.text == "📋 Kanallar ro'yxati", IsAdmin())
async def channels_list(message: Message):
    items = await db_channel_list()
    if not items:
        await message.answer("Hozircha kanal yo‘q.", reply_markup=admin_channels_menu_kb())
        return

    text = "📋 Kanallar ro'yxati:\n\n" + "\n".join(
        [f"{c.id}) {c.name}\n   tg_id: {c.telegram_id}\n   link: {c.link}" for c in items]
    )
    await message.answer(text, reply_markup=admin_channels_menu_kb())


@router.message(F.text == "➕ Kanal qo'shish", IsAdmin())
async def add_start(message: Message, state: FSMContext):
    await state.set_state(ChannelStates.add_name)
    await message.answer("Kanal nomini yubor:", reply_markup=cancel_kb())


@router.message(ChannelStates.add_name, F.text, IsAdmin())
async def add_name(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Bekor qilindi.", reply_markup=admin_channels_menu_kb())
        return

    await state.update_data(name=message.text.strip())
    await state.set_state(ChannelStates.add_telegram_id)
    await message.answer("Kanal telegram_id yubor (masalan: -1001234567890):", reply_markup=cancel_kb())


@router.message(ChannelStates.add_telegram_id, F.text, IsAdmin())
async def add_telegram_id(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Bekor qilindi.", reply_markup=admin_channels_menu_kb())
        return

    raw = message.text.strip().replace(" ", "")
    if not (raw.lstrip("-").isdigit()):
        await message.answer("telegram_id raqam bo‘lishi kerak. Qayta yubor:")
        return

    tg_id = int(raw)
    if await db_channel_exists_by_tg_id(tg_id):
        await message.answer("Bu telegram_id bazada bor. Boshqasini yubor:")
        return

    await state.update_data(telegram_id=tg_id)
    await state.set_state(ChannelStates.add_link)
    await message.answer("Kanal linkini yubor (masalan: https://t.me/kanal yoki @kanal):", reply_markup=cancel_kb())


@router.message(ChannelStates.add_link, F.text, IsAdmin())
async def add_link(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Bekor qilindi.", reply_markup=admin_channels_menu_kb())
        return

    link = message.text.strip()
    data = await state.get_data()
    await db_channel_create(
        name=data["name"],
        telegram_id=data["telegram_id"],
        link=link
    )
    await state.clear()
    await message.answer("✅ Kanal qo‘shildi!", reply_markup=admin_channels_menu_kb())


@router.message(F.text == "➖ Kanal o'chirish", IsAdmin())
async def delete_start(message: Message, state: FSMContext):
    items = await db_channel_list()
    if not items:
        await message.answer("O‘chirish uchun kanal yo‘q.", reply_markup=admin_channels_menu_kb())
        return

    await state.set_state(ChannelStates.delete_choose)
    await message.answer(
        "Qaysi kanalni o‘chirasan? (pastdan tanla)",
        reply_markup=channels_delete_inline_kb(items)
    )


@router.callback_query(ChannelStates.delete_choose, F.data.startswith("ch_del:"), IsAdminCallback())
async def delete_confirm(call: CallbackQuery, state: FSMContext):
    pk = int(call.data.split(":")[1])
    deleted = await db_channel_delete_by_id(pk)

    if deleted:
        await call.answer("O‘chirildi ✅", show_alert=False)
    else:
        await call.answer("Topilmadi ⚠️", show_alert=False)

    await state.clear()
    items = await db_channel_list()
    if not items:
        await call.message.edit_text("Hamma kanallar o‘chirildi.")
        await call.message.answer("📌 Kanal boshqaruvi:", reply_markup=admin_channels_menu_kb())
        return

    text = "📋 Qolgan kanallar:\n\n" + "\n".join([f"{c.id}) {c.name} — {c.link}" for c in items])
    await call.message.edit_text(text)
    await call.message.answer("📌 Kanal boshqaruvi:", reply_markup=admin_channels_menu_kb())


@router.callback_query(ChannelStates.delete_choose, F.data == "ch_del_cancel", IsAdminCallback())
async def delete_cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer("Bekor qilindi", show_alert=False)
    await call.message.answer("📌 Kanal boshqaruvi:", reply_markup=admin_channels_menu_kb())
