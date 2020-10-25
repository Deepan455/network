
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("upload", views.upload, name="upload"),
    path("profile/<str:name>", views.profile, name="profile"),
    path("me",views.me,name="me"),
    path("following", views.following, name="following"),
    path("follow/<str:name>",views.follow, name="follow"),
    path("unfollow/<str:name>",views.unfollow, name="unfollow"),

    #For api routes

    path("like/<str:usid>",views.like,name="like"),
    path("unlike/<str:usid>",views.unlike,name="unlike"),
]
