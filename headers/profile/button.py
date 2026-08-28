from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def profile_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄 Yangilash",
                    callback_data="profile_refresh",
                )
            ]
        ]
    )