# ============================================================
# PROFIL HANDLERI
# ============================================================
from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from .db import (
    get_profile,
    create_profile,
    username_exists,
    get_profile_stats,
)
from .button import profile_buttons
from .text import (
    PROFILE_TEXT,
    ASK_USERNAME,
    ASK_BIO,
    USERNAME_EXISTS,
    PROFILE_CREATED,
)


router = Router()


class ProfileRegistration(StatesGroup):
    username = State()
    bio = State()


def format_profile(profile, stats):
    user = profile.user

    if profile.is_premium:
        premium = "⭐ Faol"

        if profile.premium_until:
            premium_until = profile.premium_until.strftime(
                "%d.%m.%Y %H:%M"
            )
        else:
            premium_until = "Cheksiz"
    else:
        premium = "❌ Faol emas"
        premium_until = "—"

    return PROFILE_TEXT.format(
        telegram_id=user.telegram_id,
        username=profile.username,
        bio=profile.bio or "Ko‘rsatilmagan",
        balance=stats["balance"],
        premium=premium,
        premium_until=premium_until,
        referral_count=stats["referral_count"],
        subscription_count=stats["subscription_count"],
        promo_code=profile.user.telegram_id,
    )


@router.message(F.text == "👤 Profil")
async def profil(
    message: Message,
    state: FSMContext,
):
    # Eski registration state bo'lsa tozalaymiz
    await state.clear()

    profile = await get_profile(
        message.from_user.id
    )

    # Profil mavjud
    if profile:
        stats = await get_profile_stats(profile)

        await message.answer(
            format_profile(profile, stats),
            reply_markup=profile_buttons(),
        )
        return

    # Profil mavjud emas
    await state.set_state(
        ProfileRegistration.username
    )

    await message.answer(
        ASK_USERNAME
    )


@router.message(ProfileRegistration.username)
async def profile_username(
    message: Message,
    state: FSMContext,
):
    username = message.text.strip()

    # @username yuborilgan bo'lsa olib tashlaymiz
    if username.startswith("@"):
        username = username[1:]

    # Oddiy validatsiya
    if not username:
        await message.answer(
            "❌ Username bo‘sh bo‘lishi mumkin emas."
        )
        return

    if len(username) > 150:
        await message.answer(
            "❌ Username juda uzun."
        )
        return

    # Username bandligini tekshirish
    exists = await username_exists(username)

    if exists:
        await message.answer(
            USERNAME_EXISTS
        )
        return

    # Username vaqtincha FSM'da saqlanadi
    await state.update_data(
        username=username
    )

    await state.set_state(
        ProfileRegistration.bio
    )

    await message.answer(
        ASK_BIO
    )


@router.message(ProfileRegistration.bio)
async def profile_bio(
    message: Message,
    state: FSMContext,
):
    bio = message.text.strip()

    if len(bio) > 1000:
        await message.answer(
            "❌ Bio 1000 belgidan oshmasligi kerak."
        )
        return

    data = await state.get_data()

    username = data.get("username")

    if not username:
        await state.clear()

        await message.answer(
            "❌ Ro‘yxatdan o‘tishda xatolik yuz berdi. "
            "Iltimos, profilni qaytadan oching."
        )
        return

    # Profile yaratamiz
    profile = await create_profile(
        telegram_id=message.from_user.id,
        username=username,
        bio=bio,
    )

    await state.clear()

    stats = await get_profile_stats(profile)

    await message.answer(
        PROFILE_CREATED
    )

    await message.answer(
        format_profile(profile, stats),
        reply_markup=profile_buttons(),
    )


@router.callback_query(
    F.data == "profile_refresh"
)
async def profile_refresh(
    callback: CallbackQuery,
):
    profile = await get_profile(
        callback.from_user.id
    )

    if not profile:
        await callback.answer(
            "❌ Profil topilmadi.",
            show_alert=True,
        )
        return

    stats = await get_profile_stats(profile)

    await callback.message.edit_text(
        format_profile(profile, stats),
        reply_markup=profile_buttons(),
    )

    await callback.answer(
        "🔄 Profil yangilandi"
    )