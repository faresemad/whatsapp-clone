from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile/", blank=True, null=True)
    bio = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # return self.name
        return f"{self.user.username} - {self.bio:.20}"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"