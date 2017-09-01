from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from unigrin_api.models import UserProfile
from rest_framework.authtoken.models import Token


# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_userprofile(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        UserProfile.objects.create(user=instance)
