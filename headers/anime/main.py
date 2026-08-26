# ============================================================
# ANIME KO'RISH / OBUNA / YUKLAB OLISH HANDLERLARI
# ============================================================
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from asgiref.sync import sync_to_async

from main.models import Anime, Subscriptions

from ..common.filters import IsAdmin
from .db import send_anime_by_id, send_anime_epiot, send_anime_to_channel

router = Router()


@router.callback_query(F.data.startswith('anime_'))
async def inlineanime(call: CallbackQuery):
    try:
        anime_id = call.data.split('_')[1]
        await send_anime_by_id(call.message, int(anime_id))
    except Exception as e:
        print('XATO', e)


@router.callback_query(F.data.startswith('follow_'))
async def follow(call: CallbackQuery):
    try:
        anime = await sync_to_async(Anime.objects.get)(id=int(call.data.split('_')[1]))
        subscription, created = await sync_to_async(
            Subscriptions.objects.get_or_create
        )(
            telegram_user_id=call.from_user.id,
            anime=anime,
        )

        if created:
            await call.message.answer('Siz obuna bo\'ldingiz')
        else:
            await call.message.answer('Siz allaqachon obuna bo\'lgansiz!')
    except Exception as e:
        print('Obuna qo\'shishda xato:', e)
        await call.message.answer('Obuna qilishda xatolik yuz berdi.')


@router.callback_query(F.data.startswith('down_'))
async def yuklash(call: CallbackQuery):
    _, anime_id, series_numbber = call.data.split('_')
    await send_anime_epiot(call=call, anime_id=anime_id, series_id=series_numbber)


@router.message(Command('send'), IsAdmin())
async def sendanime(message: Message):
    id = message.text.split(' ')[1]
    await send_anime_to_channel(int(id))
