from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from asgiref.sync import sync_to_async

from main.models import AppLacations

from .db import get_all_channels


DEBUG_ADMIN_ID = 6491548196


async def send_debug_log(bot, text: str):
    try:
        await bot.send_message(
            chat_id=DEBUG_ADMIN_ID,
            text=text
        )
    except Exception as e:
        print(f"Debug log yuborishda xato: {e}")


async def has_pending_channel(event) -> bool:
    """
    Foydalanuvchi hali barcha majburiy kanallarga a'zo bo'lmagan
    (yoki AppLacations'da yozuvi bo'lmagan) bo'lsa True qaytaradi.
    """

    user_id = event.from_user.id

    await send_debug_log(
        event.bot,
        f"🔍 <b>SUB CHECK BOSHLANDI</b>\n\n"
        f"👤 User ID: <code>{user_id}</code>\n"
        f"📦 Event: <code>{type(event).__name__}</code>"
    )

    channels = await get_all_channels()

    await send_debug_log(
        event.bot,
        f"📋 Kanallar soni: <code>{len(channels)}</code>"
    )

    if not channels:
        await send_debug_log(
            event.bot,
            "⚠️ Majburiy kanallar topilmadi → False"
        )
        return False

    for channel in channels:
        channel_id = channel.telegram_id

        try:
            member = await event.bot.get_chat_member(
                channel_id,
                user_id
            )

            apl_exists = await sync_to_async(
                lambda: AppLacations.objects.filter(
                    user=user_id,
                    channel=channel_id
                ).exists()
            )()

            await send_debug_log(
                event.bot,
                f"🔎 <b>Kanal tekshiruvi</b>\n\n"
                f"👤 User: <code>{user_id}</code>\n"
                f"📢 Channel: <code>{channel_id}</code>\n"
                f"👤 Status: <code>{member.status}</code>\n"
                f"🗃 AppLacations: <code>{apl_exists}</code>"
            )

            if (
                member.status in (
                    "creator",
                    "administrator",
                    "member",
                    "restricted"
                )
                or apl_exists
            ):
                await send_debug_log(
                    event.bot,
                    f"✅ Kanal o'tildi: <code>{channel_id}</code>"
                )
                continue

            await send_debug_log(
                event.bot,
                f"❌ Majburiy obuna bajarilmagan!\n"
                f"📢 Channel: <code>{channel_id}</code>\n"
                f"👤 Status: <code>{member.status}</code>\n"
                f"🗃 AppLacations: <code>{apl_exists}</code>\n\n"
                f"➡️ <b>has_pending_channel = True</b>"
            )

            return True

        except Exception as e:
            await send_debug_log(
                event.bot,
                f"💥 <b>KANAL TEKSHIRISHDA XATO</b>\n\n"
                f"📢 Channel: <code>{channel_id}</code>\n"
                f"👤 User: <code>{user_id}</code>\n"
                f"❌ {type(e).__name__}: {e}\n\n"
                f"➡️ <b>has_pending_channel = True</b>"
            )

            return True

    await send_debug_log(
        event.bot,
        f"✅ <b>BARCHA KANALLAR O'TILDI</b>\n\n"
        f"👤 User: <code>{user_id}</code>\n"
        f"➡️ <b>has_pending_channel = False</b>"
    )

    return False


class call_data(BaseFilter):
    async def __call__(self, call: CallbackQuery) -> bool:
        result = await has_pending_channel(call)

        await send_debug_log(
            call.bot,
            f"🔘 <b>CALLBACK FILTER</b>\n"
            f"👤 User: <code>{call.from_user.id}</code>\n"
            f"📌 Result: <code>{result}</code>"
        )

        return result


class mess_data(BaseFilter):
    async def __call__(self, call: Message) -> bool:
        result = await has_pending_channel(call)

        await send_debug_log(
            call.bot,
            f"💬 <b>MESSAGE FILTER</b>\n"
            f"👤 User: <code>{call.from_user.id}</code>\n"
            f"📌 Result: <code>{result}</code>"
        )

        return result