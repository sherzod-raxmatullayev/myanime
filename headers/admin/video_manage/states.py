# ============================================================
# QISM (VIDEO) BOSHQARUVI STATE GROUPLARI
# ============================================================
from aiogram.fsm.state import State, StatesGroup


class AddVideoStates(StatesGroup):
    anime_id = State()
    series_number = State()
    video_file_id = State()


class DeleteVideoStates(StatesGroup):
    video_id = State()


class UploadSeries(StatesGroup):
    waiting_video = State()
