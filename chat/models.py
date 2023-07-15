from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="chatroom/", blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # return self.name
        return f"{self.name} - {self.description:.20}"

    class Meta:
        verbose_name = "Chat Room"
        verbose_name_plural = "Chat Rooms"


class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.chatroom.name} - {self.user.username} - {self.message:.20}"

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
