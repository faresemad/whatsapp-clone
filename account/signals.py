from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

# This is a receiver function that gets the signal and performs some task.
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # If the user is created, create a profile for the user.
    if created:
        Profile.objects.create(user=instance)
