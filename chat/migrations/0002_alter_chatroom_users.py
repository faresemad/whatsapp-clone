# Generated by Django 4.2 on 2023-07-16 22:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='chatrooms', to=settings.AUTH_USER_MODEL),
        ),
    ]
