# ============================================================
# QIDIRUV HANDLERLARI
# ============================================================
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from ..anime.db import send_anime_by_id
from ..common.buttons import backk
from .buttons import search_menu
from .db import search_anime_by_name_en, search_anime_by_name_uz
from .states import SearchAnime, SreachName, SreachNameen

router = Router()


@router.message(F.text == '🔍 Qidirish')
async def sreach(message: Message):
    await message.answer(text='🔍 Qidirish:', reply_markup=search_menu())


@router.message(SreachName.message)
async def search_satte(message: Message, state: FSMContext):
    text = message.text
    try:
        buttons = await search_anime_by_name_uz(text)
        if buttons is not None:
            await message.answer('Topilgan animelar', reply_markup=buttons)
        else:
            await message.answer('Animelar topilmadi')
    except Exception as e:
        print(e)
        await message.answer('Animelar topilmadi')


@router.callback_query(F.data == 'search_name_uz')
async def search(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text='Animeni qidirsh uchun uzbekcha nomini kirirtish.', reply_markup=backk())
    await state.set_state(SreachName.message)


# @router.callback_query(F.data == 'search_name_en')
# async def searchen(call: CallbackQuery, state: FSMContext):
#     await call.message.delete()
#     await call.message.answer(text='Animeni qidirsh uchun inglizcha nomini kirirtish.', reply_markup=backk())
#     await state.set_state(SreachNameen.message)


# @router.message(SreachNameen.message)
# async def search_satteen(message: Message, state: FSMContext):
#     text = message.text
#     try:
#         buttons = await search_anime_by_name_en(text)
#         if buttons is not None:
#             await message.answer('Topilgan animelar', reply_markup=buttons)
#         else:
#             await message.answer('Animelar topilmadi')
#     except Exception as e:
#         print(e)
#         await message.answer('Animelar topilmadi')


@router.callback_query(F.data == "search_kod")
async def start_search_by_id(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(SearchAnime.waiting_id)
    await call.message.edit_text(
        "🆔 Anime ID yuboring (faqat raqam).\n\n⬅️ Orqaga qaytish uchun tugmani bosing.",
        reply_markup=backk()
    )


@router.message(SearchAnime.waiting_id)
async def got_anime_id(message: Message, state: FSMContext):
    text = (message.text or "").strip()

    if not text.isdigit():
        await message.answer("❗️ID faqat raqam bo‘lishi kerak. Masalan: 12", reply_markup=backk())
        return

    anime_id = int(text)
    await send_anime_by_id(message=message, anime_id=anime_id)
    await state.clear()
