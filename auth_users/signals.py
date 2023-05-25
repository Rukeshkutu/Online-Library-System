from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile

#post_save is the signal that is sent at the end of the save method.
@receiver(post_save, sender=User)
#create_profile is the receiver function which is run every time a user is created.
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
