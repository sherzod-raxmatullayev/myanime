# ============================================================
# FALLBACK HANDLERLAR (hech qaysi filterga tushmagan xabar/callbacklar)
# ============================================================
from aiogram import Router
from aiogram.types import CallbackQuery, Message

router = Router()


@router.message()
async def test(message: Message):
    print(message.text)


@router.callback_query()
async def teees(call: CallbackQuery):
    print('CALL DATA', call.data)
