from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import *


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.contacts.set([user_profile.id])
        print('works', instance)
    if created == False:
        print('something is wrong')