from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Posts, Profile


def index(request):
    post = Posts.objects.all()
    a="nepal"
    print(a)
    
    return render(request, "network/index.html",{
        'post':reversed(post)
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def upload(request):
    if request.method == "POST":
        content = request.POST['content']
        creator = request.user.username
        likes = "10"

        #Trying to create a post
        try:
            create_post = Posts.objects.create(creator=creator,content=content,likes=likes)
            create_post.save()

        #Exception handling for failed post creation
        except Exception:
           return HttpResponse('Error creating Post')

        return HttpResponseRedirect(reverse("index")) 
    else:
        return HttpResponse('error')

@login_required
def like(request):
    liker=request.user.username 
    return HttpResponse(liker)