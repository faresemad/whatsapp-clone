from django.shortcuts import render
from .models import ChatRoom, Message
# Create your views here.
def index(request, room_name):
    try:
        room = ChatRoom.objects.get(name=room_name)
    except ChatRoom.DoesNotExist:
        return render(request, "chat/error.html", {"message": "Room does not exist."})
    return render(request, "chat/index.html", {"room": room})