# Whatsapp Clone
clone whatsapp using django and channels
## Basic Setup & Installation
```bash
python -m pip install -U channels["daphne"]
```

- Add `dephne` to `INSTALLED_APPS` in `settings.py`
```python
INSTALLED_APPS = (
    "daphne",
    ...
)
```
- Then, adjust your project’s `asgi.py` file, e.g. `project/asgi.py`, to wrap the Django ASGI application:
```python
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from channels.auth import AuthMiddlewareStack
import chat.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))
        ),
    }
)
```

- Add `ASGI_APPLICATION` to `settings.py`
```python
ASGI_APPLICATION = "project.routing.application"
```
## Implement a Chat Server
- Create a new file called `consumer.py` in the `chat` app directory, and add the following code:
```python
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, ChatRoom
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"][
            "room_name"
        ]  # get room name from url
        self.room_group_name = "chat_%s" % self.room_name  # create group name
        self.user = self.scope["user"]  # get user from scope

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # accept connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from websocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]  # get message from json

        # Save message to database
        await self.save_message(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",  # call chat_message method
                "message": message,
                "user": self.user.username,
                "room": self.room_name,
            },
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]  # get message from event
        user = event["user"]  # get user from event
        room = event["room"]  # get room from event

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps({"message": message, "user": user, "room": room})
        )

    @database_sync_to_async
    def save_message(self, message):
        user = User.objects.get(username=self.user.username)
        room = ChatRoom.objects.get(name=self.room_name)
        message = message
        if message != "":
            Message.objects.create(user=user, chatroom=room, message=message)
        return True
```
- Create a new file called `routing.py` in the `chat` app directory, and add the following code:
```python
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
```
## Enable a channel layer
- Add `CHANNEL_LAYERS` to `settings.py`
```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}
```
## Create a ChatRoom model
- Create a new file called `models.py` in the `chat` app directory, and add the following code:
```python
class ChatRoom(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="chatrooms", blank=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="chatroom/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Chat Room"
        verbose_name_plural = "Chat Rooms"
```
## Create a Message model
- Create a new file called `models.py` in the `chat` app directory, and add the following code:
```python
class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.chatroom.name} - {self.user.username}"

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
```
## Create a ChatRoomForm
- Create a new file called `forms.py` in the `chat` app directory, and add the following code:
```python
class ChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ["name", "image", "description"]
        ...
        ...
```

## Create a Room (Detail/List) View
- Create a new file called `views.py` in the `chat` app directory, and add the following code:
```python
@login_required
def room_detail(request, room_name):
    if not request.user.is_authenticated:
        return redirect("account:login")
    try:
        # check if current user in chat room users
        room = ChatRoom.objects.get(name=room_name, users=request.user)
        if room:
            messages = Message.objects.filter(chatroom=room)
        else:
            messages = None
    except ChatRoom.DoesNotExist:
        return render(request, "chat/error.html", {"message": "Room does not exist or you are not a member of this room"})
    return render(request, "chat/chat.html", {"room_name": room.name, "messages": messages})

@login_required
def room_list(request):
    if not request.user.is_authenticated:
        return redirect("account:login")
    rooms = ChatRoom.objects.filter(users=request.user)
    return render(request, "chat/chats.html", {"rooms": rooms})
```
- Create a new file called `urls.py` in the `chat` app directory, and add the following code:
```python
from django.urls import path
from .views import room_detail, room_list

app_name = "chat"
urlpatterns = [
    path("<str:room_name>/", room_detail, name="room_detail"),
    path("list", room_list, name="room_list"),
]
```
- Add `chat` urls to `project/urls.py`
```python
urlpatterns = [
    ...
    path("", include(("chat.urls", "chat"), namespace="chat")),
    ...
]
```
## Create a ChatRoomForm
- Create a new file called `forms.py` in the `chat` app directory, and add the following code:
```python
class ChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ["name", "image", "description"]
        ...
        ...
```