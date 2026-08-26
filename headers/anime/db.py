# ============================================================
# ANIME YUBORISH / KO'RSATISH DB FUNKSIYALARI
# ============================================================
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from asgiref.sync import sync_to_async
from django.db.models import F as DjangoF

from loader import bot
from main.models import Anime, Video

from ..common.constants import CHANNEL_ID
from .buttons import build_anime_view_keyboard, build_download_button


@sync_to_async
def search_anime_by_id(anime_id: int):
    return Anime.objects.filter(id=anime_id).first()


@sync_to_async
def anime_exists(anime_id: int) -> bool:
    return Anime.objects.filter(id=anime_id).exists()


async def send_anime_by_id(message: Message, anime_id: int):
    anime = await search_anime_by_id(anime_id=anime_id)

    if not anime:
        await message.answer('Anime topilmadi')
        return

    # Bir nechta foydalanuvchi bir vaqtda ko‘rsa ham view yo‘qolib ketmasin.
    await sync_to_async(
        lambda: Anime.objects.filter(id=anime.id).update(views=DjangoF('views') + 1)
    )()
    anime.views += 1

    text = (
        f'ID {anime.id}\n\n'
        f"🎬 <b>{anime.name_uz}</b>\n\n"
        # f"🌍 <b>English:</b> {anime.name_en}\n"
        f"🎭 <b>Janr:</b> {anime.janr}\n"
        f"📅 <b>Yil:</b> {anime.year}\n"
        f"📺 <b>Qismlar soni:</b> {anime.series_count}\n"
        f"👁 <b>Ko‘rishlar:</b> {anime.views}\n\n"
        f"📝 <b>Duberlar:</b>\n{anime.discreptin}"
    )
    if anime.photo_id:
        await message.answer_photo(
            photo=anime.photo_id,
            caption=text,
            parse_mode='HTML',
            reply_markup=build_anime_view_keyboard(anime.id)
        )


async def send_anime_to_channel(anime_id: int):
    """
    Berilgan anime_id bo'yicha anime ma'lumotlarini bazadan olib,
    kanalga rasm va caption bilan yuboradi. Inline tugma orqali Yuklash mumkin.
    """
    anime = await sync_to_async(lambda: Anime.objects.get(id=anime_id))()
    if not anime:
        return False  # Anime topilmadi

    caption = (
        f"🆔 ID: {anime.id}\n\n"
        f"🎬 <b>{anime.name_uz}</b>\n"
        # f"🇺🇸 <i>{anime.name_en}</i>\n\n"
        f"📖 <b>Duberlar:</b>\n{anime.discreptin}\n\n"
        f"🎭 <b>Janr:</b> {anime.janr}\n"
        f"📅 <b>Yil:</b> {anime.year}\n"
        f"🎞 <b>Qismlar soni:</b> {anime.series_count}\n"
        f"👁 <b>Ko‘rishlar:</b> {anime.views}"
    )

    # Views ni +1 qilish (parallel xavfsiz). `F` shu yerda lokal import
    # qilinadi, chunki aiogram'ning global `F` magic filter'i bilan
    # nom to'qnashmasligi kerak.
    from django.db.models import F
    await sync_to_async(lambda: Anime.objects.filter(id=anime.id).update(views=F('views') + 1))()

    await bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=anime.photo_id,
        caption=caption,
        parse_mode="HTML",
        reply_markup=build_download_button(anime.id)
    )
    return True


async def send_anime_epiot(call: CallbackQuery, anime_id, series_id):
    vedios = await sync_to_async(list)(Video.objects.filter(
        anime=anime_id
    ).order_by('series_number'))
    await call.message.delete()
    video = await sync_to_async(
        Video.objects.filter(
            anime=anime_id,
            series_number=series_id
        ).first
    )()
    if not video:
        await call.answer('Bu qism mavjud emas.', show_alert=True)
        return

    ved = video.video_file_id

    kb = InlineKeyboardBuilder()
    for butt in vedios:
        if butt.series_number == int(series_id):
            kb.button(
                text=f'[{butt.series_number}]',
                callback_data='null'
            )
        else:
            kb.button(
                text=f'{butt.series_number}',
                callback_data=f'down_{anime_id}_{butt.series_number}'
            )
    kb.adjust(6)

    await call.bot.send_video(
        chat_id=call.from_user.id,
        video=ved,
        caption=f'Anime ID: {video.id}',
        reply_markup=kb.as_markup()
    )
