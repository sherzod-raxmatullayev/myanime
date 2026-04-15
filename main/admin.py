from django.contrib import admin
from .models import TelegramUsers, Channels, AppLacations, Anime, Video
# Register your models here.

admin.site.register(TelegramUsers)
admin.site.register(Channels)
admin.site.register(AppLacations)
admin.site.register(Anime)
admin.site.register(Video)