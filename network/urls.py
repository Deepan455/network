from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all_posts", views.all_posts,name="all_posts"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("upload", views.upload, name="upload"),
    path("post/<str:psid>",views.post,name="post"),
    path("profile/<str:name>", views.profile, name="profile"),
    path("me",views.me,name="me"),
    path("following", views.following, name="following"),
    path("follow/<str:name>",views.follow, name="follow"),
    path("unfollow/<str:name>",views.unfollow, name="unfollow"),
    path("edit/",views.edit,name="edit"),
    path("delete/<str:psid>",views.delete, name="delete"),

    #For api routes

    path("like/<str:psid>",views.like,name="like"),
    path("unlike/<str:psid>",views.unlike,name="unlike"),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)