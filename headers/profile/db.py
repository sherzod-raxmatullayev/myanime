from asgiref.sync import sync_to_async

from main.models import (
    TelegramUsers,
    Profile,
    Referal,
    Subscriptions,
)


@sync_to_async
def get_user(telegram_id: int):
    return TelegramUsers.objects.filter(
        telegram_id=telegram_id
    ).first()


@sync_to_async
def get_profile(telegram_id: int):
    return Profile.objects.select_related("user").filter(
        user__telegram_id=telegram_id
    ).first()


@sync_to_async
def create_profile(
    telegram_id: int,
    username: str,
    bio: str,
):
    user = TelegramUsers.objects.filter(
        telegram_id=telegram_id
    ).first()

    if not user:
        user = TelegramUsers.objects.create(
            telegram_id=telegram_id
        )

    profile = Profile.objects.create(
        user=user,
        username=username,
        bio=bio,
    )

    return profile


@sync_to_async
def username_exists(username: str):
    return Profile.objects.filter(
        username=username
    ).exists()


@sync_to_async
def get_profile_stats(profile: Profile):
    user = profile.user

    referral_count = Referal.objects.filter(
        referrer=user
    ).count()

    subscription_count = Subscriptions.objects.filter(
        telegram_user_id=user.telegram_id
    ).count()

    return {
        "balance": user.balance,
        "referral_count": referral_count,
        "subscription_count": subscription_count,
    }