from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("chat:room_list"))
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password == password2:
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.save()
            return HttpResponseRedirect(reverse("account:login"))
        else:
            return HttpResponse("Password is not match")
    else:
        return render(request, "account/register.html", {})


def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("chat:room_list"))
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print(username, password)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("chat:room_list"))
            else:
                return HttpResponse("User is not active")
        else:
            return HttpResponse("User is None")
    else:
        return render(request, "account/login.html", {})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("account:login"))
