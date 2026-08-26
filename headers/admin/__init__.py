# ============================================================
# ADMIN ROUTERLARINI BIRLASHTIRISH
# ============================================================
from aiogram import Router

from .anime_manage.main import router as anime_manage_router
from .backup.main import router as backup_router
from .broadcast.main import router as broadcast_router
from .channels.main import router as channels_router
from .panel.main import router as panel_router
from .stats.main import router as stats_router
from .video_manage.main import router as video_manage_router

router = Router()
router.include_router(panel_router)
router.include_router(anime_manage_router)
router.include_router(video_manage_router)
router.include_router(channels_router)
router.include_router(broadcast_router)
router.include_router(stats_router)
router.include_router(backup_router)
