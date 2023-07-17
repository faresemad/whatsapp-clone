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

