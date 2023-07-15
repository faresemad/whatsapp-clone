from django.urls import path
from .views import signup, login_user, logout_user

app_name = "account"

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login_user, name="login_user"),
    path("logout/", logout_user, name="logout_user"),
]
