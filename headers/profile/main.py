from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from .db import get_profile, create_profile, username_exists, get_profile_stats
from .button import profile_buttons
from .text import PROFILE_TEXT, ASK_USERNAME, ASK_BIO, USERNAME_EXISTS, PROFILE_CREATED


router = Router()


class ProfileRegistration(StatesGroup):
    username = State()
    bio = State()


def format_profile(profile, stats):
    user = profile.user
    if profile.is_premium:
        premium = "⭐ Faol"
        premium_until = (
            profile.premium_until.strftime("%d.%m.%Y %H:%M")
            if profile.premium_until else "Cheksiz"
        )
    else:
        premium, premium_until = "❌ Faol emas", "—"

    return PROFILE_TEXT.format(
        telegram_id=user.telegram_id,
        username=profile.username,
        bio=profile.bio or "Ko‘rsatilmagan",
        balance=stats["balance"],
        premium=premium,
        premium_until=premium_until,
        referral_count=stats["referral_count"],
        subscription_count=stats["subscription_count"],
        promo_code=profile.promo_code,
    )


@router.message(F.text == "👤 Profil")
async def profil(message: Message, state: FSMContext):
    await state.clear()
    profile = await get_profile(message.from_user.id)

    if profile:
        stats = await get_profile_stats(profile)
        await message.answer(
            format_profile(profile, stats),
            reply_markup=profile_buttons()
        )
        return

    await state.set_state(ProfileRegistration.username)
    await message.answer(ASK_USERNAME)


@router.message(ProfileRegistration.username)
async def profile_username(message: Message, state: FSMContext):
    username = message.text.strip().lstrip("@")

    if not username:
        await message.answer("❌ Username bo‘sh bo‘lishi mumkin emas.")
        return

    if len(username) > 150:
        await message.answer("❌ Username juda uzun.")
        return

    if await username_exists(username):
        await message.answer(USERNAME_EXISTS)
        return

    await state.update_data(username=username)
    await state.set_state(ProfileRegistration.bio)
    await message.answer(ASK_BIO)


@router.message(ProfileRegistration.bio)
async def profile_bio(message: Message, state: FSMContext):
    bio = message.text.strip()

    if len(bio) > 1000:
        await message.answer("❌ Bio 1000 belgidan oshmasligi kerak.")
        return

    data = await state.get_data()
    username = data.get("username")

    if not username:
        await state.clear()
        await message.answer(
            "❌ Xatolik yuz berdi. Profilni qaytadan oching."
        )
        return

    profile = await create_profile(
        telegram_id=message.from_user.id,
        username=username,
        bio=bio,
    )

    await state.clear()
    stats = await get_profile_stats(profile)

    await message.answer(PROFILE_CREATED)
    await message.answer(
        format_profile(profile, stats),
        reply_markup=profile_buttons()
    )


@router.callback_query(F.data == "profile_refresh")
async def profile_refresh(callback: CallbackQuery):
    profile = await get_profile(callback.from_user.id)

    if not profile:
        await callback.answer(
            "❌ Profil topilmadi.",
            show_alert=True
        )
        return

    stats = await get_profile_stats(profile)

    await callback.message.edit_text(
        format_profile(profile, stats),
        reply_markup=profile_buttons()
    )
    await callback.answer("🔄 Profil yangilandi")