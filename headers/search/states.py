# ============================================================
# QIDIRUV STATE GROUPLARI
# ============================================================
from aiogram.fsm.state import State, StatesGroup


class SreachName(StatesGroup):
    message = State()


class SreachNameen(StatesGroup):
    message = State()


class SearchAnime(StatesGroup):
    waiting_id = State()
