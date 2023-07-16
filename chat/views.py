from django.shortcuts import render, redirect
from .models import ChatRoom
from .forms import ChatRoomForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def room_detail(request, room_name):
    if not request.user.is_authenticated:
        return redirect("account:login")
    try:
        # check if current user in chat room users
        room = ChatRoom.objects.get(name=room_name, users=request.user)
    except ChatRoom.DoesNotExist:
        return render(request, "chat/error.html", {"message": "Room does not exist or you are not a member of this room"})
    return render(request, "chat/chat.html", {"room": room})

@login_required
def room_list(request):
    if not request.user.is_authenticated:
        return redirect("account:login")
    rooms = ChatRoom.objects.filter(users=request.user)
    return render(request, "chat/chats.html", {"rooms": rooms})

@login_required
def create_chat_room(request):
    # check if user authenticated and if not redirect to login page
    if not request.user.is_authenticated:
        return redirect("account:login")
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
    return render(request, "chat/create_chat.html", {"form": form})
