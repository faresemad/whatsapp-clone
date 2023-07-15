from django.shortcuts import render
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
            login(request, new_user)
            return HttpResponseRedirect(reverse("chat:chatroom_list"))
    else:
        form = SignUpForm()
    return render(request, "account/signup.html", {"form": form})

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print(username, password)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("chat:chatroom_list"))
            else:
                return HttpResponse("User is not active")
        else:
            return HttpResponse("User is None")
    else:
        return render(request, "account/login.html", {})

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("account:login_user"))