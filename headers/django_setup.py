# ============================================================
# DJANGO SOZLAMALARINI ISHGA TUSHIRISH
# (modellardan foydalanishdan oldin shart)
# ============================================================
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()
