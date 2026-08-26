# ============================================================
# KUZATILAYOTGANLAR HANDLERLARI
# ============================================================
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from .buttons import sub_menu
from .db import delete_subscription, get_user_subscriptions

router = Router()


@router.message(F.text == '📺 Kuzatilayotgan')
async def kuzatilganlar(message: Message):
    user_animes = await get_user_subscriptions(message.from_user.id)
    if not user_animes:
        await message.answer('Siz hali animelarga obuna bo\'lmagansiz')
    for item in user_animes:
        await message.answer(f'Anime: {item.anime.name_uz}', reply_markup=sub_menu(item.id))


@router.callback_query(F.data.startswith('del_'))
async def deletes(call: CallbackQuery):
    await call.message.delete()
    id = call.data.split('_')[1]
    deleted = await delete_subscription(id, call.from_user.id)

    if deleted:
        await call.message.answer('O\'chirildi!')
    else:
        await call.message.answer('Xatolik yoki bu obuna sizga tegishli emas.')
