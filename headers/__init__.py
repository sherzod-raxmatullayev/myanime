# ============================================================
# HEADERS PAKETI — barcha bo'lim routerlarini bitta routerga yig'adi
# ============================================================
# Django modellardan foydalanishdan oldin sozlamalarni ishga
# tushiramiz (bu import shart ravishda eng birinchi bo'lishi kerak).
from . import django_setup  # noqa: F401

from aiogram import Router

from .admin import router as admin_router
from .anime.main import router as anime_router
from .contact.main import router as contact_router
from .fallback.main import router as fallback_router
from .profile.main import router as profile_router
from .search.main import router as search_router
from .start.main import router as start_router
from .subscription.main import router as subscription_router
from .watchlist.main import router as watchlist_router

router = Router()

# Tartib MUHIM — aiogram handlerlarni registratsiya tartibida tekshiradi:
#   1) majburiy obuna tekshiruvi eng birinchi bo'lishi kerak
#   2) fallback (catch-all) handlerlar esa eng oxirida bo'lishi kerak
router.include_router(subscription_router)
router.include_router(start_router)
router.include_router(anime_router)
router.include_router(watchlist_router)
router.include_router(profile_router)
router.include_router(contact_router)
router.include_router(admin_router)
router.include_router(search_router)
router.include_router(fallback_router)
