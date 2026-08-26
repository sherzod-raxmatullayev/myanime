# ============================================================
# UMUMIY FILTERLAR (admin tekshiruvi)
# ============================================================
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

from .constants import ADMIN_ID


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in [6950463049,]


class IsAdminCallback(BaseFilter):
    async def __call__(self, call: CallbackQuery) -> bool:
        return call.from_user.id == ADMIN_ID
