from django.urls import path
from .views import room_detail, room_list, create_chat_room

app_name = "chat"
urlpatterns = [
    path("room/<str:room_name>/", room_detail, name="index"),
    path("list/", room_list, name="room_list"),
    path("create/", create_chat_room, name="create_chat_room"),
]
