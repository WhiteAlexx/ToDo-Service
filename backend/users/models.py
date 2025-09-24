from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token


class User(AbstractUser):

    telegram_id = models.PositiveBigIntegerField(primary_key=True, verbose_name='Telegram ID')

    id = None

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['telegram_id']

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return str(self.username)


# Signal for automatic token creation upon user creation
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):

    if created:
        Token.objects.create(user=instance)
