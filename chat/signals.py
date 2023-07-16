from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ChatRoom

@receiver(post_save, sender=ChatRoom)
def add_creator_to_users(sender, instance, created, **kwargs):
    if created:
        instance.users.add(instance.creator)
        instance.save()
