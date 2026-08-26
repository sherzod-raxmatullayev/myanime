# ============================================================
# ANIME QO'SHISH/O'CHIRISH STATE GROUPLARI
# ============================================================
from aiogram.fsm.state import State, StatesGroup


class AddAnimeStates(StatesGroup):
    name_uz = State()
    name_en = State()
    discreptin = State()
    janr = State()
    year = State()
    series_count = State()
    photo_id = State()


class DeleteAnimeStates(StatesGroup):
    anime_id = State()
