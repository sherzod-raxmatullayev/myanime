

from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
import uuid

# Create your models here.
class TelegramUsers(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return f"User {self.telegram_id} - Balance: {self.balance}"

    # ✅ Pul qo‘shish funksiyasi
    def add_balance(self, amount: int):
        if amount > 0:
            self.balance += amount
            self.save()
            return True
        return False

    # ✅ Pul ayirish funksiyasi (minusga tushib ketmasligi uchun himoyalangan)
    def remove_balance(self, amount: int):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False

    # ✅ Balans yetarlimi tekshiruvchi funksiya
    def has_enough_balance(self, amount: int):
        return self.balance >= amount
    


    # Kanallar ro'yxati
class Channels(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    telegram_id = models.BigIntegerField()
    link = models.TextField()

    def __str__(self):
        return f"Channel {self.name}"


# Ilovalar/abonentlar
class AppLacations(models.Model):
    user = models.BigIntegerField()
    channel = models.BigIntegerField()

    def __str__(self):
        return f"User {self.user} in Channel {self.channel}"
    







class Anime(models.Model):
    '''Animeni asosiy modeli'''
    name_uz = models.CharField(max_length=255, verbose_name='Nomi (Uzbek)')
    name_en = models.CharField(max_length=255, verbose_name='Nomi (Ingliz)')
    discreptin = models.TextField(verbose_name='Tavsif')
    janr = models.TextField()
    year = models.CharField(max_length=4)
    series_count = models.IntegerField(default=0)
    photo_id = models.TextField()
    views = models.IntegerField(default=0)



class Video(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    series_number = models.IntegerField()
    video_file_id = models.TextField()


class Subscriptions(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    telegram_user_id = models.BigIntegerField()

    class Meta:
        unique_together = ('anime', 'telegram_user_id')

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(TelegramUsers, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, blank=True, null=True, unique=True)
    bio = models.TextField(blank=True)
    is_premium = models.BooleanField(default=False)
    premium_until = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Referal(models.Model):
    referrer = models.ForeignKey(TelegramUsers, related_name='referrals', on_delete=models.CASCADE)
    referred = models.ForeignKey(TelegramUsers, related_name='referred_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('referrer', 'referred')