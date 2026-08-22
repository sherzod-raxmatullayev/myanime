from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from aiogram.types import Update

from loader import bot, dp
import bot_setup

@csrf_exempt
async def telegram_webhook(request):
    if request.method != 'POST':
        return HttpResponse("Method Not Allowed", status=405)

    update = Update.model_validate_json(
        request.body
    )
    await dp.feed_update(bot, update)
    return HttpResponse("OK", status=200)