# ============================================================
# ADMIN: QISM (VIDEO) BOSHQARUVI HANDLERLARI
# ============================================================
import asyncio

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ...anime.buttons import build_download_button, build_series_download_keyboard
from ...common.buttons import backk
from ...common.constants import CHANNEL_ID
from ...common.filters import IsAdmin
from .buttons import qisim_settings_keyboard
from .db import (
    add_video,
    anime_exists,
    create_video,
    delete_video,
    get_anime,
    get_next_series_number,
    get_subscribers,
    video_exists,
)
from .states import AddVideoStates, DeleteVideoStates, UploadSeries

router = Router()


@router.message(F.text == '🧩 Qism sozlamalari', IsAdmin())
async def admin_series_setting(message: Message, state: FSMContext):
    await message.answer('🧩 Qism sozlamalari', reply_markup=qisim_settings_keyboard)


@router.message(F.text == "➕ Video qo'shish", IsAdmin())
async def start_add_video(message: Message, state: FSMContext):
    await message.answer("🔢 Anime ID sini kiriting:")
    await state.set_state(AddVideoStates.anime_id)


@router.message(AddVideoStates.anime_id, IsAdmin())
async def process_video_anime_id(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Iltimos, to'g'ri ID kiriting:")
        return

    anime_id = int(message.text)
    exists = await anime_exists(anime_id)

    if not exists:
        await message.answer("⚠️ Bunday ID li Anime topilmadi!")
        await state.set_state(AddVideoStates.anime_id)
        return

    await state.update_data(anime_id=anime_id)
    await message.answer("🔢 Seriya raqamini kiriting:")
    await state.set_state(AddVideoStates.series_number)


@router.message(AddVideoStates.series_number, IsAdmin())
async def process_series_number(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Iltimos, to'g'ri raqam kiriting:")
        return

    await state.update_data(series_number=int(message.text))
    await message.answer("🎥 Video faylni yuboring:")
    await state.set_state(AddVideoStates.video_file_id)


@router.message(AddVideoStates.video_file_id, IsAdmin())
async def process_video_file(message: Message, state: FSMContext):
    if not message.video:
        await message.answer("⚠️ Iltimos, video fayl yuboring:")
        return

    video_file_id = message.video.file_id
    data = await state.get_data()

    anime = await get_anime(data['anime_id'])
    subscribers = await get_subscribers(anime.id)

    await create_video(
        anime=anime,
        series_number=data['series_number'],
        video_file_id=video_file_id
    )

    caption = (
            f"🆕 <b>Yangi qism qo‘shildi!</b>\n\n"
            f"🎬 <b>{anime.name_uz}</b>\n"
            # f"🇺🇸 <i>{anime.name_en}</i>\n\n"
            f"🎞 <b>Qism:</b> {data['series_number']}\n"
            f"🆔 <b>Anime ID:</b> {anime.id}\n\n"
            f"🍿 Yangi qismni hoziroq tomosha qiling!"
        )

    if not message.caption:
        await message.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=anime.photo_id,
            caption=caption,
            reply_markup=build_download_button(anime.id),
            parse_mode='HTML'
        )

    for sub in subscribers:
        try:
            await message.bot.send_photo(
                chat_id=sub.telegram_user_id,
                photo=anime.photo_id,
                caption=caption,
                reply_markup=build_series_download_keyboard(anime.id),
                parse_mode='HTML'
            )
            await asyncio.sleep(0.2)
        except Exception:
            pass

    await message.answer("✅ Video muvaffaqiyatli qo'shildi!")
    await state.clear()


@router.message(F.text == "🗑 Video o'chirish", IsAdmin())
async def start_delete_video(message: Message, state: FSMContext):
    await message.answer("🔢 O'chirmoqchi bo'lgan Video ID sini kiriting:")
    await state.set_state(DeleteVideoStates.video_id)


@router.message(DeleteVideoStates.video_id, IsAdmin())
async def process_delete_video(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Iltimos, to'g'ri ID kiriting:")
        return

    video_id = int(message.text)
    exists = await video_exists(video_id)

    if not exists:
        await message.answer("⚠️ Bunday ID li Video topilmadi!")
        await state.clear()
        return

    await delete_video(video_id)
    await message.answer(f"✅ ID: {video_id} - Video muvaffaqiyatli o'chirildi!")
    await state.clear()


@router.message(Command("animedow"), IsAdmin())
async def animedow_cmd(message: Message, state: FSMContext):
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip().isdigit():
        await message.answer("Foydalanish: /animedow <anime_id>\nMasalan: /animedow 12")
        return

    anime_id = int(parts[1].strip())

    if not await anime_exists(anime_id):
        await message.answer("❌ Bunday ID bilan anime yo‘q.")
        return

    next_series = await get_next_series_number(anime_id)

    await state.set_state(UploadSeries.waiting_video)
    await state.update_data(anime_id=anime_id, next_series=next_series)

    await message.answer(
        f"✅ Anime ID={anime_id}\n"
        f"📥 Hozir {next_series}-qismni yubor.\n\n"
        f"⬅️ Chiqish uchun Back.",
        reply_markup=backk()
    )


@router.message(UploadSeries.waiting_video, IsAdmin())
async def got_series_video(message: Message, state: FSMContext):
    data = await state.get_data()
    anime_id = data.get("anime_id")
    next_series = data.get("next_series")

    # Video file_id olish (qaysi turda yuborganiga qarab)
    file_id = None
    if message.video:
        file_id = message.video.file_id
    elif message.document:
        # odamlar ko'pincha videoni "file" sifatida yuboradi
        file_id = message.document.file_id

    if not file_id:
        await message.answer(
            f"❗️Bu video emas. Iltimos {next_series}-qism videosini yubor (video yoki file ko‘rinishida).",
            reply_markup=backk()
        )
        return

    await add_video(anime_id=anime_id, series_number=next_series, file_id=file_id)
    next_series += 1
    await state.update_data(next_series=next_series)

    await message.answer(
        f"✅ Saqlandi: Anime ID={anime_id}, {next_series-1}-qism.\n"
        f"📥 Endi {next_series}-qismni yubor.\n\n"
        f"⬅️ Chiqish uchun Back.",
        reply_markup=backk()
    )
