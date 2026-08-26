# ============================================================
# ADMIN: ANIME BOSHQARUVI HANDLERLARI
# ============================================================
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ...anime.buttons import build_download_button
from ...common.buttons import backk
from ...common.constants import CHANNEL_ID
from ...common.filters import IsAdmin
from .buttons import anime_settings_keyboard
from .db import anime_exists, create_anime, delete_anime
from .states import AddAnimeStates, DeleteAnimeStates

router = Router()


@router.message(F.text == '🎬 Anime sozlamalari', IsAdmin())
async def anime_sozlamalari(message: Message):
    await message.answer('🎬 Anime sozlamalari', reply_markup=anime_settings_keyboard)


@router.message(F.text == '➕ Anime qo‘shish', IsAdmin())
async def start_add_anime(message: Message, state: FSMContext):
    await message.answer("📝 Animening uzbekcha nomini kiriting:", reply_markup=backk())
    await state.set_state(AddAnimeStates.name_uz)


@router.message(AddAnimeStates.name_uz, IsAdmin())
async def process_name_uz(message: Message, state: FSMContext):
    await state.update_data(name_uz=message.text)
    await message.answer("📝 Animening inglizcha nomini kiriting:", reply_markup=backk())
    await state.set_state(AddAnimeStates.name_en)


@router.message(AddAnimeStates.name_en, IsAdmin())
async def process_name_en(message: Message, state: FSMContext):
    await state.update_data(name_en=message.text)
    await message.answer("📄 Anime haqida duberlarni yozing:", reply_markup=backk())
    await state.set_state(AddAnimeStates.discreptin)


@router.message(AddAnimeStates.discreptin, IsAdmin())
async def process_discreptin(message: Message, state: FSMContext):
    await state.update_data(discreptin=message.text)
    await message.answer("🎭 Anime janrini kiriting:", reply_markup=backk())
    await state.set_state(AddAnimeStates.janr)


@router.message(AddAnimeStates.janr, IsAdmin())
async def process_janr(message: Message, state: FSMContext):
    await state.update_data(janr=message.text)
    await message.answer("📅 Anime chiqgan yilini kiriting:", reply_markup=backk())
    await state.set_state(AddAnimeStates.year)


@router.message(AddAnimeStates.year, IsAdmin())
async def process_year(message: Message, state: FSMContext):
    if not message.text.isdigit() or len(message.text) != 4:
        await message.answer("⚠️ Iltimos, to'g'ri yil formatini kiriting (4 ta raqam):", reply_markup=backk())
        return

    await state.update_data(year=message.text)
    await message.answer("🎬 Seriyalar sonini kiriting:", reply_markup=backk())
    await state.set_state(AddAnimeStates.series_count)


@router.message(AddAnimeStates.series_count, IsAdmin())
async def process_series_count(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Iltimos, to'g'ri son kiriting:", reply_markup=backk())
        return

    await state.update_data(series_count=int(message.text))
    await message.answer("🖼 Anime rasmini yuboring:", reply_markup=backk())
    await state.set_state(AddAnimeStates.photo_id)


@router.message(AddAnimeStates.photo_id, IsAdmin())
async def process_photo_id(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("⚠️ Iltimos, rasm yuboring:", reply_markup=backk())
        return

    photo_id = message.photo[-1].file_id
    await state.update_data(photo_id=photo_id)
    data = await state.get_data()

    anime = await create_anime(data)

    caption = (
        f'ID: {anime.id}\n\n'
        f"🎬 <b>{data['name_uz']}</b>\n"
        f"🇺🇸 <i>{data['name_en']}</i>\n\n"
        f"📖 <b>Tavsif:</b>\n{data['discreptin']}\n\n"
        f"🎭 <b>Janr:</b> {data['janr']}\n"
        f"📅 <b>Yil:</b> {data['year']}\n"
        f"🎞 <b>Qismlar soni:</b> {data['series_count']}"
    )

    await message.bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=data['photo_id'],
        caption=caption,
        parse_mode="HTML",
        reply_markup=build_download_button(anime.id)
    )
    await message.answer("✅ Anime muvaffaqiyatli qo'shildi!")
    await state.clear()


@router.message(F.text == "🗑 Anime o'chirish", IsAdmin())
async def start_delete_anime(message: Message, state: FSMContext):
    await message.answer("🔢 O'chirmoqchi bo'lgan Anime ID sini kiriting:")
    await state.set_state(DeleteAnimeStates.anime_id)


@router.message(DeleteAnimeStates.anime_id, IsAdmin())
async def process_delete_anime(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Iltimos, to'g'ri ID kiriting:")
        return

    anime_id = int(message.text)
    exists = await anime_exists(anime_id)

    if not exists:
        await message.answer("⚠️ Bunday ID li Anime topilmadi!")
        await state.set_state(DeleteAnimeStates.anime_id)
        return

    await delete_anime(anime_id)
    await message.answer(f"✅ ID: {anime_id} - Anime muvaffaqiyatli o'chirildi!")
    await state.clear()
