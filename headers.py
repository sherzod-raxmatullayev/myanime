from ast import Delete, Is
from csv import Error
from email import message
from re import A
import time
from tkinter import Button
from unittest import result
from aiogram.types import Message, CallbackQuery, ChatJoinRequest
from aiogram.filters import Command, CommandStart
from aiogram import Router, F
import asyncio
from asgiref.sync import sync_to_async

from aiogram.filters import BaseFilter


from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

import json


DEVLOPER_ID = 6950463049

router = Router()



class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in [6950463049]
    


import os
import django

# 1️⃣ Django settings modulini ko‘rsatish
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# 2️⃣ Django muhitini ishga tushirish
django.setup()

# 3️⃣ Endi modellardan import qilish mumkin
from main.models import TelegramUsers, Anime, AppLacations, Channels, Video, Subscriptions
from asgiref.sync import sync_to_async

from loader import bot




async def button(user_id: int, referal) -> InlineKeyboardMarkup | None:
    kb = InlineKeyboardBuilder()

    channels = await sync_to_async(lambda: list(Channels.objects.all()))()
    if not channels:
        return None

    for channel in channels:
        channel_id = channel.telegram_id
        try:
            member = await bot.get_chat_member(channel_id, user_id)
            apl_exists = await sync_to_async(lambda: AppLacations.objects.filter(
                user=user_id, channel=channel_id
            ).exists())()

            if member.status in ("creator", "administrator", "member", "restricted") or apl_exists:
                continue
            else:
                kb.button(text=channel.name, url=channel.link)

        except Exception:
            kb.button(text=channel.name, url=channel.link)
    if referal != None:
        kb.button(text='✅ Tekshirish', callback_data=f'tekshir_{referal}')
    else:
        kb.button(text='✅ Tekshirish', callback_data=f'start')
        

    if kb:  
        return kb.adjust(1)


class call_data(BaseFilter):
    async def __call__(self, call: CallbackQuery) -> bool:
        user_id = call.from_user.id

        # Barcha kanallarni olish (sync → async)
        channels = await sync_to_async(lambda: list(Channels.objects.all()))()
        if not channels:
            return False

        for channel in channels:
            channel_id = channel.telegram_id  # ORM field

            try:
                # Bot bilan tekshirish (async)
                member = await call.bot.get_chat_member(channel_id, user_id)

                # Applications da foydalanuvchi borligini tekshirish (sync → async)
                apl_exists = await sync_to_async(lambda: AppLacations.objects.filter(
                    user=user_id, channel=channel_id
                ).exists())()

                # Agar foydalanuvchi kanal a'zos bo'lsa yoki apl mavjud bo'lsa skip
                if member.status in ("creator", "administrator", "member", "restricted") or apl_exists:
                    continue
                else:
                    return True  # foydalanuvchi a'zo emas va application mavjud emas

            except Exception:
                # Xatolik bo‘lsa, filter False qaytarsin
                return False

        return False
class mess_data(BaseFilter):
    async def __call__(self, call: Message) -> bool:
        user_id = call.from_user.id

        # Barcha kanallarni olish (sync → async)
        channels = await sync_to_async(lambda: list(Channels.objects.all()))()
        if not channels:
            return False

        for channel in channels:
            channel_id = channel.telegram_id  # ORM field

            try:
                # Bot bilan tekshirish (async)
                member = await call.bot.get_chat_member(channel_id, user_id)

                # Applications da foydalanuvchi borligini tekshirish (sync → async)
                apl_exists = await sync_to_async(lambda: AppLacations.objects.filter(
                    user=user_id, channel=channel_id
                ).exists())()

                # Agar foydalanuvchi kanal a'zos bo'lsa yoki apl mavjud bo'lsa skip
                if member.status in ("creator", "administrator", "member", "restricted") or apl_exists:
                    continue
                else:
                    return True  # foydalanuvchi a'zo emas va application mavjud emas

            except Exception:
                # Xatolik bo‘lsa, filter False qaytarsin
                return False

        return False






@router.message(mess_data())
async def mandatory_message(message: Message):
    referel = None
    if message.text.startswith('/start'):
        full_args = message.text.split(' ')
        if len(full_args) > 1:
            _, referel = full_args
    kb = await button(message.from_user.id, referel)
    if kb:
        await message.answer("Iltimos, quyidagi kanallarga obuna bo'ling va tekshirishni  bosing:", reply_markup=kb.as_markup())

@router.callback_query(call_data())
async def mandatory_callback(query: CallbackQuery):
    kb = await button(query.from_user.id, None)
    if kb:
        await query.answer("Iltimos, quyidagi kanallarga obuna bo'ling va /start bosing.", reply_markup=kb.as_markup())








@router.chat_join_request(F.chat.type.in_({"supergroup", "channel"}))
async def handle_join_request(event: ChatJoinRequest):
    await sync_to_async(lambda: AppLacations.objects.create(user = event.from_user.id, channel = event.chat.id))()



@router.callback_query(F.data == 'start')
async def inlinestart(message: CallbackQuery):
    try:
        user, created = await sync_to_async(lambda: TelegramUsers.objects.get_or_create(
            telegram_id=message.from_user.id
        ))()
        if created:
            text_new_user = (
                f"Yangi foydalanuvchi qo'shildi\n\n"
                f"ID: {message.from_user.id}\n"
                f"Full name: {message.from_user.first_name}\n"
            )
            await message.bot.send_message(chat_id=DEVLOPER_ID, text=text_new_user)
        await message.message.delete()
        await message.message.answer("Asosiy sahifa!")
    except Exception as e:
        print('inline startda xato', e)
        await message.message.answer("Asosiy sahifa!")




@sync_to_async
def search_anime_by_id(anime_id:int):
    return Anime.objects.filter(id=anime_id).first()

    
async def send_anime_by_id(message: Message, anime_id : int):
    anime = await search_anime_by_id(anime_id=anime_id)
    anime.views += 1
    await sync_to_async(anime.save)()

    if not anime:
        await message.answer('Anime topilmadi')
        return
    
    def button(anime_id):
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
    text='⭐ Kuzatish',
    callback_data=f'follow_{anime_id}'
)
, InlineKeyboardButton(
    text='⬇️ Yuklash',
    callback_data=f'down_{anime_id}_1'
)]
            ]
        )


    text = (
        f'ID {anime.id}\n\n'
        f"🎬 <b>{anime.name_uz}</b>\n\n"
        f"🌍 <b>English:</b> {anime.name_en}\n"
        f"🎭 <b>Janr:</b> {anime.janr}\n"
        f"📅 <b>Yil:</b> {anime.year}\n"
        f"📺 <b>Qismlar soni:</b> {anime.series_count}\n"
        f"👁 <b>Ko‘rishlar:</b> {anime.views}\n\n"
        f"📝 <b>Duberlar:</b>\n{anime.discreptin}"
    )
    if anime.photo_id:
        await message.answer_photo(photo=anime.photo_id, caption=text, parse_mode='HTML', reply_markup=button(anime.id))





main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔍 Qidirish")],                 # 1-qator
        [
            KeyboardButton(text="📺 Kuzatilayotgan"),         # 2-qator
            KeyboardButton(text="👤 Profil")
        ],
        [KeyboardButton(text="📩 Aloqa")]                     # 3-qator
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)



@router.callback_query(F.data.startswith('anime_'))
async def inlineanime(call:CallbackQuery):
    try:
        id = call.data.split('_')[1]
        await send_anime_by_id(call.message, int(id))
    except Exception as e:
        print('XATO', e)


@router.message(CommandStart())
async def inlinestart(message: Message):
    try:
        if len(message.text.split(' ')) == 2:
            id = message.text.split(' ')[1]
            await send_anime_by_id(message=message, anime_id=int(id))

        user, created = await sync_to_async(lambda: TelegramUsers.objects.get_or_create(
            telegram_id=message.from_user.id
        ))()
        if created:
            text_new_user = (
    "━━━━━━━━━━━━━━\n"
    "🆕 *Yangi foydalanuvchi*\n"
    "━━━━━━━━━━━━━━\n\n"
    f"🆔 ID: `{message.from_user.id}`\n"
    f"👤 To‘liq ism: {message.from_user.first_name}"
)



            await message.bot.send_message(chat_id=DEVLOPER_ID, text=text_new_user)
   
        await message.answer("Asosiy sahifa!", reply_markup=main_menu)
    except Exception as e:
        print('inline startda xato', e)
        await message.answer("Asosiy sahifa!", reply_markup=main_menu)


def search_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text='🔍 Uzbekcha nomi bilan qidirish', callback_data='search_name_uz')
    kb.button(text='🔍 Inglizcha nomi bilan qidirish', callback_data='search_name_en')
    kb.button(text='🔍 Kodi bilan qidirish', callback_data='search_kod')
    kb.button(text='🔍 Janri bilan qidirish', callback_data='search_janr')
    kb.button(text='Orqaga', callback_data='back')
    return kb.adjust(1).as_markup()



def backk():
    kb = InlineKeyboardBuilder()
    kb.button(text='Orqaga', callback_data='back')
    return kb.adjust(1).as_markup()



@router.callback_query(F.data == 'back')
async def closes(call:CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.delete()
    await call.message.answer("Asosiy sahifa!", reply_markup=main_menu)





#  QIDIRUV START

@router.message(F.text == '🔍 Qidirish')
async def sreach(message:Message):
    await message.answer(text='🔍 Qidirish:', reply_markup=search_menu())






class SreachName(StatesGroup):
    message = State()


class SreachNameen(StatesGroup):
    message = State()



@router.callback_query(F.data == 'search_name_uz')
async def search(call:CallbackQuery, state:FSMContext):
    await call.message.delete()
    await call.message.answer(text='Animeni qidirsh uchun uzbekcha nomini kirirtish.', reply_markup=backk())
    await state.set_state(SreachName.message)

@router.callback_query(F.data == 'search_name_en')
async def searchen(call:CallbackQuery, state:FSMContext):
    await call.message.delete()
    await call.message.answer(text='Animeni qidirsh uchun inglizcha nomini kirirtish.', reply_markup=backk())
    await state.set_state(SreachNameen.message)



@sync_to_async
def search_anime_by_name_uz(query: str, limit: int = 10):
    """
    Anime qidirish va inline tugmalar generatsiya qilish
    """

    animes = list(
        Anime.objects.filter(name_uz__icontains=query)
        .values('id', 'name_uz')[:limit]
    )
    
    if not animes:
        return None
    

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    for anime in animes:
        button = InlineKeyboardButton(
            text=anime['name_uz'],
            callback_data=f"anime_{anime['id']}"
        )
        keyboard.inline_keyboard.append([button])
    but = InlineKeyboardButton(
        text='Orqaga',
        callback_data='back'
    )
    keyboard.inline_keyboard.append([but])
    
    return keyboard



@sync_to_async
def search_anime_by_name_en(query: str, limit: int = 10):
    """
    Anime qidirish va inline tugmalar generatsiya qilish
    """

    animes = list(
        Anime.objects.filter(name_en__icontains=query)
        .values('id', 'name_en')[:limit]
    )
    
    if not animes:
        return None
    

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    for anime in animes:
        button = InlineKeyboardButton(
            text=anime['name_en'],
            callback_data=f"anime_{anime['id']}"
        )
        keyboard.inline_keyboard.append([button])
    but = InlineKeyboardButton(
        text='Orqaga',
        callback_data='back'
    )
    keyboard.inline_keyboard.append([but])
    
    
    return keyboard





@router.callback_query(F.data.startswith('follow_'))
async def follow(call:CallbackQuery):
    try:
        anime = await sync_to_async(Anime.objects.get)(id=int(call.data.split('_')[1]))
        subscription = await sync_to_async(Subscriptions.objects.create)(
        telegram_user_id=call.from_user.id,
        anime=anime)
        await call.message.answer('Siz obuna bo\'ldingiz')
    except Exception as e:
        await call.message.answer(f'Siz allaqachon obuna bo\'lgansiz!')





# QIDRUV END



# ADMIN START


admin_panel_buttons = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text='🎬 Anime sozlamalari'),
            KeyboardButton(text='🧩 Qism sozlamalari')
        ],
        [
            KeyboardButton(text='📢 Kanal sozlamalari'),
            KeyboardButton(text='📨 Xabar tarqatish')
        ],
        [
            KeyboardButton(text='📊 Statistika'),
            KeyboardButton(text='👥 Foydalanuvchini boshqarish')
        ]
    ]
)



@router.message(Command('panel'), IsAdmin())
async def adminpanel(message:Message):
    await message.answer('Admin panel', reply_markup=admin_panel_buttons)      



@router.message(F.text == '⬅️ Orqaga', IsAdmin())
async def backirqaadmin(message:Message, state:FSMContext):
    await message.delete()
    await state.clear()
    await message.answer('Admin panel', reply_markup=admin_panel_buttons)


anime_settings_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text='➕ Anime qo‘shish'),
            KeyboardButton(text="🗑 Anime o'chirish")
        ],
        [
            KeyboardButton(text='⬅️ Orqaga')
        ]
    ]
)


qisim_settings_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="➕ Video qo'shish"),
            KeyboardButton(text="🗑 Video o'chirish")
        ],
        [
            KeyboardButton(text='⬅️ Orqaga')
        ]
    ]
)


@router.message(F.text == '🎬 Anime sozlamalari', IsAdmin())
async def anime_sozlamalari(message:Message):
    await message.answer('🎬 Anime sozlamalari', reply_markup=anime_settings_keyboard)


@router.message(F.text == '🧩 Qism sozlamalari', IsAdmin())
async def admin_series_setting(message:Message, state:FSMContext):
    await message.answer('🧩 Qism sozlamalari', reply_markup=qisim_settings_keyboard)



class AddAnimeStates(StatesGroup):
    name_uz = State()
    name_en = State()
    discreptin = State()
    janr = State()
    year = State()
    series_count = State()
    photo_id = State()


@router.message(F.text == '➕ Anime qo‘shish', IsAdmin())
async def start_add_anime(message: Message, state: FSMContext):
    await message.answer("📝 Animening uzbekcha nomini kiriting:", reply_markup=backk())
    await state.set_state(AddAnimeStates.name_uz)


# name_uz qabul qilish
@router.message(AddAnimeStates.name_uz)
async def process_name_uz(message: Message, state: FSMContext):
    await state.update_data(name_uz=message.text)
    await message.answer("📝 Animening inglizcha nomini kiriting:", reply_markup=backk())
    await state.set_state(AddAnimeStates.name_en)


# name_en qabul qilish
@router.message(AddAnimeStates.name_en)
async def process_name_en(message: Message, state: FSMContext):
    await state.update_data(name_en=message.text)
    await message.answer("📄 Anime haqida duberlarni yozing:", reply_markup=backk())
    await state.set_state(AddAnimeStates.discreptin)


# discreptin qabul qilish
@router.message(AddAnimeStates.discreptin)
async def process_discreptin(message: Message, state: FSMContext):
    await state.update_data(discreptin=message.text)
    await message.answer("🎭 Anime janrini kiriting:", reply_markup=backk())
    await state.set_state(AddAnimeStates.janr)


# janr qabul qilish
@router.message(AddAnimeStates.janr)
async def process_janr(message: Message, state: FSMContext):
    await state.update_data(janr=message.text)
    await message.answer("📅 Anime chiqgan yilini kiriting:", reply_markup=backk())
    await state.set_state(AddAnimeStates.year)


# year qabul qilish
@router.message(AddAnimeStates.year)
async def process_year(message: Message, state: FSMContext):
    if not message.text.isdigit() or len(message.text) != 4:
        await message.answer("⚠️ Iltimos, to'g'ri yil formatini kiriting (4 ta raqam):", reply_markup=backk())
        return
    
    await state.update_data(year=message.text)
    await message.answer("🎬 Seriyalar sonini kiriting:", reply_markup=backk())
    await state.set_state(AddAnimeStates.series_count)


# series_count qabul qilish
@router.message(AddAnimeStates.series_count)
async def process_series_count(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Iltimos, to'g'ri son kiriting:", reply_markup=backk())
        return
    
    await state.update_data(series_count=int(message.text))
    await message.answer("🖼 Anime rasmini yuboring:", reply_markup=backk())
    await state.set_state(AddAnimeStates.photo_id)


# photo_id qabul qilish va saqlash
@router.message(AddAnimeStates.photo_id)
async def process_photo_id(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("⚠️ Iltimos, rasm yuboring:", reply_markup=backk())
        return
    
    photo_id = message.photo[-1].file_id
    await state.update_data(photo_id=photo_id)
    
    # Ma'lumotlarni olish
    data = await state.get_data()
    
    # Bazaga saqlash
    anime = await sync_to_async(Anime.objects.create)(
        name_uz=data['name_uz'],
        name_en=data['name_en'],
        discreptin=data['discreptin'],
        janr=data['janr'],
        year=data['year'],
        series_count=data['series_count'],
        photo_id=data['photo_id']
    )
    # 📢 Kanal uchun post matni
    caption = (
        f'ID: {anime.id}\n\n'
        f"🎬 <b>{data['name_uz']}</b>\n"
        f"🇺🇸 <i>{data['name_en']}</i>\n\n"
        f"📖 <b>Tavsif:</b>\n{data['discreptin']}\n\n"
        f"🎭 <b>Janr:</b> {data['janr']}\n"
        f"📅 <b>Yil:</b> {data['year']}\n"
        f"🎞 <b>Qismlar soni:</b> {data['series_count']}"
    )


    def down_bu(anime_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='⬇️ Yuklash',
                        url=f'https://t.me/anibox_dbbot?start={anime_id}'
                    )
                ]
            ]
        )

    # 📤 Kanalga yuborish
    await message.bot.send_photo(
        chat_id=-1001954758682,
        photo=data['photo_id'],
        caption=caption,
        parse_mode="HTML",
        reply_markup=down_bu(anime.id)
    )
    await message.answer("✅ Anime muvaffaqiyatli qo'shildi!")
    await state.clear()

class DeleteAnimeStates(StatesGroup):
    anime_id = State()


@router.message(F.text == "🗑 Anime o'chirish")
async def start_delete_anime(message: Message, state: FSMContext):
    await message.answer("🔢 O'chirmoqchi bo'lgan Anime ID sini kiriting:")
    await state.set_state(DeleteAnimeStates.anime_id)


# Anime o'chirish
@router.message(DeleteAnimeStates.anime_id)
async def process_delete_anime(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Iltimos, to'g'ri ID kiriting:")
        return
    
    anime_id = int(message.text)
    
    # Anime mavjudligini tekshirish
    anime_exists = await sync_to_async(Anime.objects.filter(id=anime_id).exists)()
    
    if not anime_exists:
        await message.answer("⚠️ Bunday ID li Anime topilmadi!")
        await state.set_state(DeleteAnimeStates.anime_id)
        return
    
    # Anime o'chirish
    await sync_to_async(Anime.objects.filter(id=anime_id).delete)()
    
    await message.answer(f"✅ ID: {anime_id} - Anime muvaffaqiyatli o'chirildi!")
    await state.clear()

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async

CHANNEL_ID = -1001954758682  # O‘z kanaling ID sini qo‘y

async def send_anime_to_channel(anime_id: int):
    """
    Berilgan anime_id bo‘yicha anime ma'lumotlarini bazadan olib,
    kanalga rasm va caption bilan yuboradi.
    Inline tugma orqali Yuklash mumkin.
    """
    # Anime obyektini olish
    anime = await sync_to_async(lambda: Anime.objects.get(id=anime_id))()

    if not anime:
        return False  # Anime topilmadi

    # Kanalga yuborish uchun caption
    caption = (
        f"🆔 ID: {anime.id}\n\n"
        f"🎬 <b>{anime.name_uz}</b>\n"
        f"🇺🇸 <i>{anime.name_en}</i>\n\n"
        f"📖 <b>Duberlar:</b>\n{anime.discreptin}\n\n"
        f"🎭 <b>Janr:</b> {anime.janr}\n"
        f"📅 <b>Yil:</b> {anime.year}\n"
        f"🎞 <b>Qismlar soni:</b> {anime.series_count}\n"
        f"👁 <b>Ko‘rishlar:</b> {anime.views}"
    )

    # Inline tugma funksiyasi
    def down_bu(anime_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='⬇️ Yuklash',
                        url=f'https://t.me/anibox_dbbot?start={anime_id}'
                    )
                ]
            ]
        )

    # Views ni +1 qilish (parallel xavfsiz)
    from django.db.models import F
    await sync_to_async(lambda: Anime.objects.filter(id=anime.id).update(views=F('views') + 1))()

    # Kanalga yuborish
    await bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=anime.photo_id,
        caption=caption,
        parse_mode="HTML",
        reply_markup=down_bu(anime.id)
    )

    return True


@router.message(Command('send'), IsAdmin())
async def sendanime(message:Message):
    id = message.text.split(' ')[1]
    await send_anime_to_channel(int(id))



class AddVideoStates(StatesGroup):
    anime_id = State()
    series_number = State()
    video_file_id = State()

class DeleteVideoStates(StatesGroup):
    video_id = State()

@router.message(F.text == "➕ Video qo'shish")
async def start_add_video(message: Message, state: FSMContext):
    await message.answer("🔢 Anime ID sini kiriting:")
    await state.set_state(AddVideoStates.anime_id)


# Anime ID qabul qilish
@router.message(AddVideoStates.anime_id)
async def process_video_anime_id(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Iltimos, to'g'ri ID kiriting:")
        return
    
    anime_id = int(message.text)
    
    # Anime mavjudligini tekshirish
    anime_exists = await sync_to_async(Anime.objects.filter(id=anime_id).exists)()
    
    
    if not anime_exists:
        await message.answer("⚠️ Bunday ID li Anime topilmadi!")
        await state.set_state(AddVideoStates.anime_id)
        return
    
    await state.update_data(anime_id=anime_id)
    await message.answer("🔢 Seriya raqamini kiriting:")
    await state.set_state(AddVideoStates.series_number)


# Seriya raqami qabul qilish
@router.message(AddVideoStates.series_number)
async def process_series_number(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Iltimos, to'g'ri raqam kiriting:")
        return
    
    await state.update_data(series_number=int(message.text))
    await message.answer("🎥 Video faylni yuboring:")
    await state.set_state(AddVideoStates.video_file_id)


# Video fayl qabul qilish va saqlash
@router.message(AddVideoStates.video_file_id)
async def process_video_file(message: Message, state: FSMContext):
    if not message.video:
        await message.answer("⚠️ Iltimos, video fayl yuboring:")
        return
    
    video_file_id = message.video.file_id
    data = await state.get_data()
    
    # Animeni olish
    anime = await sync_to_async(Anime.objects.get)(id=data['anime_id'])
    
    subscribers = await sync_to_async(list)(
    Subscriptions.objects.filter(anime_id=anime.id)
)
    # Video saqlash
    await sync_to_async(Video.objects.create)(
        anime=anime,
        series_number=data['series_number'],
        video_file_id=video_file_id
    )

    caption = (
        f'✅ Yangi qisim qo\'shildi\n'
        f'ID: {anime.id}\n'
        f"🎬 <b>{anime.name_uz}</b>\n"
        f"🇺🇸 <i>{anime.name_en}</i>\n"
        f"🎞 <b>Qism:</b> {data['series_number']}\n\n"

    )
    def down_bu(anime_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='⬇️ Yuklash',
                        url=f'https://t.me/anibox_dbbot?start={anime_id}'
                    )
                ]
            ]
        )
    if not message.caption:
        await message.bot.send_photo(
            chat_id=-1001954758682,
            photo=anime.photo_id,
            caption=caption,
            reply_markup=down_bu(anime.id),
            parse_mode='HTML'
        )

    def button(anime_id):
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
    text='⬇️ Yuklash',
    callback_data=f'down_{anime_id}_1'
)]
            ]
        )


    for sub in subscribers:
        try:
            await message.bot.send_photo(
            chat_id=sub.telegram_user_id,
            photo=anime.photo_id,
            caption=caption,
            reply_markup=button(anime.id),
            parse_mode='HTML'
        )
            time.sleep(0.2)

        except:
            pass
    
    
    await message.answer("✅ Video muvaffaqiyatli qo'shildi!")
    await state.clear()


# Video o'chirish boshlash
@router.message(F.text == "🗑 Video o'chirish")
async def start_delete_video(message: Message, state: FSMContext):
    await message.answer("🔢 O'chirmoqchi bo'lgan Video ID sini kiriting:")
    await state.set_state(DeleteVideoStates.video_id)


# Video o'chirish
@router.message(DeleteVideoStates.video_id)
async def process_delete_video(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Iltimos, to'g'ri ID kiriting:")
        return
    
    video_id = int(message.text)
    
    # Video mavjudligini tekshirish
    video_exists = await sync_to_async(Video.objects.filter(id=video_id).exists)()
    
    if not video_exists:
        await message.answer("⚠️ Bunday ID li Video topilmadi!")
        await state.clear()
        return
    
    # Video o'chirish
    await sync_to_async(Video.objects.filter(id=video_id).delete)()
    
    await message.answer(f"✅ ID: {video_id} - Video muvaffaqiyatli o'chirildi!")
    await state.clear()

# ADMIN END



async def send_anime_epiot(call: CallbackQuery, anime_id, series_id):
    vedios = await sync_to_async(list)(Video.objects.filter(
        anime = anime_id
    ).order_by('series_number'))
    await call.message.delete()
    video = await sync_to_async(
    Video.objects.filter(
        anime=anime_id,
        series_number=series_id
                    ).first
                )()
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




@router.callback_query(F.data.startswith('down_'))
async def yuklash(call:CallbackQuery):
    _, anime_id, series_numbber = call.data.split('_')
    await send_anime_epiot(call=call, anime_id=anime_id, series_id=series_numbber)

  


@router.message(SreachName.message)
async def search_satte(message:Message, state:FSMContext):
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
    

@router.message(SreachNameen.message)
async def search_satteen(message:Message, state:FSMContext):
    text = message.text
    try:
        buttons = await search_anime_by_name_en(text)
        if buttons is not None:
            await message.answer('Topilgan animelar', reply_markup=buttons)
        else:
            await message.answer('Animelar topilmadi')
    except Exception as e:
        print(e)
        await message.answer('Animelar topilmadi')


def sub_menu(id):
    kb = InlineKeyboardBuilder()
    kb.button(
        text='O\'chirish',
        callback_data=f'del_{id}'
    )
    kb.adjust(1)
    return kb.as_markup()


@router.message(F.text == '📺 Kuzatilayotgan')
async def kuzatilganlar(message:Message):
    user_animes = await sync_to_async(list)(Subscriptions.objects.filter(telegram_user_id=message.from_user.id).select_related('anime'))
    if not user_animes:
        await message.answer('Siz hali animelarga obuna bo\'lmagansiz')
    for item in user_animes:
        await message.answer(f'Anime: {item.anime.name_uz}', reply_markup=sub_menu(item.id))


@router.callback_query(F.data.startswith('del_'))
async def deletes(call:CallbackQuery):
    await call.message.delete()
    id = call.data.split('_')[1]
    result = await sync_to_async(Subscriptions.objects.filter(id = id).delete)()
    if result:
        await call.message.answer('O\'chirildi!')
    else:
        await call.message.answer('Xatolik')



@router.message(F.text == '👤 Profil')
async def profil(message:Message):
    await message.answer('Bu qisim hali tayyor emas!')

@router.message(F.text == '📩 Aloqa')
async def aloqa(message:Message):
    await message.answer('Aloqa uchun admin: @sherzod_raxmatullayev')






# ---------- STATES ----------
class ChannelStates(StatesGroup):
    add_name = State()
    add_telegram_id = State()
    add_link = State()
    delete_choose = State()

# ---------- ORM HELPERS (async wrappers) ----------
@sync_to_async
def db_channel_create(name: str, telegram_id: int, link: str) -> Channels:
    return Channels.objects.create(name=name, telegram_id=telegram_id, link=link)

@sync_to_async
def db_channel_list():
    return list(Channels.objects.all().order_by("id"))

@sync_to_async
def db_channel_delete_by_id(pk: int) -> int:
    deleted, _ = Channels.objects.filter(id=pk).delete()
    return deleted

@sync_to_async
def db_channel_exists_by_tg_id(tg_id: int) -> bool:
    return Channels.objects.filter(telegram_id=tg_id).exists()

# ---------- KEYBOARDS ----------
def admin_channels_menu_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="➕ Kanal qo'shish")
    kb.button(text="➖ Kanal o'chirish")
    kb.button(text="📋 Kanallar ro'yxati")
    kb.button(text="⬅️ Orqaga")
    kb.adjust(2, 1)
    return kb.as_markup(resize_keyboard=True)

def cancel_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="❌ Bekor qilish")
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

# ---------- COMMAND / MENU ----------
@router.message(F.text == '📢 Kanal sozlamalari', IsAdmin())
async def channels_admin_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("📌 Kanal boshqaruvi:", reply_markup=admin_channels_menu_kb())

# ---------- LIST ----------
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

# ---------- ADD FLOW ----------
@router.message(F.text == "➕ Kanal qo'shish", IsAdmin())
async def add_start(message: Message, state: FSMContext):
    await state.set_state(ChannelStates.add_name)
    await message.answer("Kanal nomini yubor:", reply_markup=cancel_kb())

@router.message(ChannelStates.add_name, F.text)
async def add_name(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Bekor qilindi.", reply_markup=admin_channels_menu_kb())
        return

    await state.update_data(name=message.text.strip())
    await state.set_state(ChannelStates.add_telegram_id)
    await message.answer("Kanal telegram_id yubor (masalan: -1001234567890):", reply_markup=cancel_kb())

@router.message(ChannelStates.add_telegram_id, F.text)
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

@router.message(ChannelStates.add_link, F.text)
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

# ---------- DELETE FLOW ----------
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

@router.callback_query(ChannelStates.delete_choose, F.data.startswith("ch_del:"))
async def delete_confirm(call: CallbackQuery, state: FSMContext):
    pk = int(call.data.split(":")[1])
    deleted = await db_channel_delete_by_id(pk)

    if deleted:
        await call.answer("O‘chirildi ✅", show_alert=False)
    else:
        await call.answer("Topilmadi ⚠️", show_alert=False)

    await state.clear()
    # qayta ro'yxat ko'rsatib yuboramiz
    items = await db_channel_list()
    if not items:
        await call.message.edit_text("Hamma kanallar o‘chirildi.")
        await call.message.answer("📌 Kanal boshqaruvi:", reply_markup=admin_channels_menu_kb())
        return

    text = "📋 Qolgan kanallar:\n\n" + "\n".join([f"{c.id}) {c.name} — {c.link}" for c in items])
    await call.message.edit_text(text)
    await call.message.answer("📌 Kanal boshqaruvi:", reply_markup=admin_channels_menu_kb())

@router.callback_query(ChannelStates.delete_choose, F.data == "ch_del_cancel")
async def delete_cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer("Bekor qilindi", show_alert=False)
    await call.message.answer("📌 Kanal boshqaruvi:", reply_markup=admin_channels_menu_kb())




import os
import io
import zipfile
from datetime import datetime

from django.core.management import call_command
from aiogram.types import BufferedInputFile


ADMIN_ID = 6950463049  # <-- o'zingning Telegram ID'ing


@sync_to_async
def make_full_dump_json_bytes() -> bytes:
    """
    Django dumpdata -> JSON bytes (butun baza data)
    """
    buf = io.StringIO()

    # dumpdata barcha app/model datani chiqaradi
    # exclude: auth.permission va contenttypes (xohlasang olib tashlash mumkin)
    call_command(
        "dumpdata",
        "--natural-foreign",
        "--natural-primary",
        "--indent",
        "2",
        exclude=["contenttypes", "auth.permission"],
        stdout=buf
    )

    return buf.getvalue().encode("utf-8")


def zip_bytes(filename: str, data: bytes) -> bytes:
    """
    JSON bytes -> ZIP bytes
    """
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr(filename, data)
    return out.getvalue()


@router.message(F.text == "/sos")
async def sos_backup_handler(message: Message):
    # Faqat admin ishlatsin (xohlamasang olib tashla)
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Bu buyruq faqat admin uchun.")
        return

    await message.answer("🧯 Backup tayyorlanmoqda...")

    json_bytes = await make_full_dump_json_bytes()

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    json_name = f"db_backup_{stamp}.json"
    zip_name = f"db_backup_{stamp}.zip"

    zipped = zip_bytes(json_name, json_bytes)

    # Telegramga ZIP fayl yuboramiz (JSON katta bo'lishi mumkin)
    file = BufferedInputFile(zipped, filename=zip_name)

    await message.bot.send_document(
        chat_id=ADMIN_ID,
        document=file,
        caption=f"✅ DB Backup (dumpdata) | {stamp}\n📦 {zip_name}"
    )

    await message.answer("✅ Backup yuborildi.")




class messagesClass(StatesGroup):
    mess = State()








@router.message(messagesClass.mess)
async def message_state(message: Message, state: FSMContext):
    users = await sync_to_async(lambda: list(TelegramUsers.objects.all()))()


    error = 0
    count = 0

    for user in users:
        try:
            # ✅ AGAR XABAR MATN BO'LSA
            if message.text:
                await message.bot.send_message(
                    chat_id=user.telegram_id,
                    text=message.text
                )

            # ✅ AGAR XABAR RASM BO'LSA
            elif message.photo:
                await message.bot.send_photo(
                    chat_id=user.telegram_id,
                    photo=message.photo[-1].file_id,
                    caption=message.caption if message.caption else None
                )

            # ✅ AGAR XABAR VIDEO BO'LSA (ixtiyoriy)
            elif message.video:
                await message.bot.send_video(
                    chat_id=user.telegram_id,
                    video=message.video.file_id,
                    caption=message.caption if message.caption else None
                )

            count += 1
            await asyncio.sleep(0.1)

        except Exception as e:
            print('Xabar tarqatishda muamo:', e)
            error += 1

    await message.answer(
        text=f"✅ Xabar yetkazildi: {count}\n❌ Tarqatilmadi: {error}",
        reply_markup=admin_panel_buttons
    )

    await state.clear()




@router.message(F.text == "📨 Xabar tarqatish", IsAdmin())
async def tarqart(message:Message, state: FSMContext):
    await message.answer(text="Tarqatmoqchi bo'lgan xabaringizni yuboring.", reply_markup=back)
    await state.set_state(messagesClass.mess)




# ---- ORM stats ----
@sync_to_async
def db_get_stats():
    return {
        "users": TelegramUsers.objects.count(),
        "anime": Anime.objects.count(),
        "apps": AppLacations.objects.count(),
        "channels": Channels.objects.count(),
        "videos": Video.objects.count(),
        "subs": Subscriptions.objects.count(),
    }

# ---- handler: 📊 Statistika ----
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




class SearchAnime(StatesGroup):
    waiting_id = State()

@router.callback_query(F.data == "search_kod")
async def start_search_by_id(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(SearchAnime.waiting_id)
    await call.message.edit_text(
        "🆔 Anime ID yuboring (faqat raqam).\n\n⬅️ Orqaga qaytish uchun tugmani bosing.",
        reply_markup=backk()  # callback_data='back' bo'lishi shart
    )

@router.message(SearchAnime.waiting_id)
async def got_anime_id(message: Message, state: FSMContext):
    text = (message.text or "").strip()

    if not text.isdigit():
        await message.answer("❗️ID faqat raqam bo‘lishi kerak. Masalan: 12", reply_markup=backk())
        return

    anime_id = int(text)

    # Sening tayyor funksiyang:
    await send_anime_by_id(message=message, anime_id=anime_id)

    # Qidiruv tugadi (xohlasang state'ni qoldirsa ham bo'ladi)
    await state.clear()




class UploadSeries(StatesGroup):
    waiting_video = State()




@sync_to_async
def anime_exists(anime_id: int) -> bool:
    return Anime.objects.filter(id=anime_id).exists()

@sync_to_async
def get_next_series_number(anime_id: int) -> int:
    m = Video.objects.filter(anime_id=anime_id).aggregate(Max("series_number"))["series_number__max"]
    return (m or 0) + 1

@sync_to_async
def add_video(anime_id: int, series_number: int, file_id: str):
    return Video.objects.create(
        anime_id=anime_id,
        series_number=series_number,
        video_file_id=file_id
    )
from django.db.models import Max



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


@router.message(UploadSeries.waiting_video)
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

    # Keyingi qismga o'tkazamiz
    next_series += 1
    await state.update_data(next_series=next_series)

    await message.answer(
        f"✅ Saqlandi: Anime ID={anime_id}, {next_series-1}-qism.\n"
        f"📥 Endi {next_series}-qismni yubor.\n\n"
        f"⬅️ Chiqish uchun Back.",
        reply_markup=backk()
    )


@router.message()
async def  test(message:Message):
    print(message.text)

@router.callback_query()
async def teees(call:CallbackQuery):
    print('CALL DATA', call.data)