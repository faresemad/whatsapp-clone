from django.shortcuts import render, redirect
from .models import ChatRoom
from .forms import ChatRoomForm


# Create your views here.
def room_detail(request, room_name):
    try:
        room = ChatRoom.objects.get(name=room_name)
    except ChatRoom.DoesNotExist:
        return render(request, "chat/error.html", {"message": "Room does not exist."})
    return render(request, "chat/index.html", {"room": room})


def room_list(request):
    rooms = ChatRoom.objects.get(creator=request.user)
    return render(request, "chat/room_list.html", {"rooms": rooms})


def create_chat_room(request):
    if request.method == "POST":
        form = ChatRoomForm(request.POST, request.FILES)
        if form.is_valid():
            chat_room = form.save(commit=False)
            chat_room.creator = request.user
            chat_room.save()
            form.save_m2m()
            return redirect("chat:index", room_name=chat_room.name)
    else:
        form = ChatRoomForm()
    return render(request, "chat/create_chat_room.html", {"form": form})
