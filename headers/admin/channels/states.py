# ============================================================
# KANAL BOSHQARUVI STATE GROUPI
# ============================================================
from aiogram.fsm.state import State, StatesGroup


class ChannelStates(StatesGroup):
    add_name = State()
    add_telegram_id = State()
    add_link = State()
    delete_choose = State()
