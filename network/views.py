from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Posts


def index(request):
    post = Posts.objects.all()
    me=request.user.username
    print("hello")
    print(me)
    person=User.objects.get(username=me)
    my_liked=person.likers.all()
    print(my_liked)
    return render(request, "network/index.html",{
        'post':reversed(post),
        'my_liked':my_liked
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
        person = request.user.username
        creator = User.objects.get(username=person)
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

def profile(request,name):
    me=request.user.username
    person=User.objects.get(username=me)
    pro=User.objects.get(username=name)
    email=pro.email
    posts=pro.profile.all()
    followers=pro.followers.all()
    following=pro.following.all()
    my_liked=person.likers.all()
    my_following=person.following.all()
    return render(request,"network/profile.html",{
        "profile":pro,
        "name":name,
        "email":email,
        "post":posts,
        "followers":followers,
        "following":following,
        "my_liked":my_liked,
        "my_following":my_following
        })

def following(request):
    me=request.user.username
    print (me)
    pro=User.objects.get(username=me)
    following=pro.following.all()
    my_liked=pro.likers.all()
    n=0
    basket=[]
    for spam in following:
        cheese=Posts.objects.filter(creator=spam)
        if n==0:
            basket=cheese
        else:
            basket=basket | cheese
        n+=1

    print(basket)
    print(reversed(basket))
    return render(request,"network/index.html",{
        'post':reversed(basket),
        'my_liked':my_liked
        })

@login_required
def follow(request,name):
    me=request.user.username
    if(name!=me):
        pro=User.objects.get(username=me)
        tofollow=User.objects.get(username=name)
        pro.following.add(tofollow)
        pro.save()
        message="you now follow "+name
        return JsonResponse({"message":message})
    else:
        return JsonResponse({"message":"You cannot follow yourself"})

@login_required
def unfollow(request,name):
    me=request.user.username
    if(name!=me):
        pro=User.objects.get(username=me)
        tofollow=User.objects.get(username=name)
        pro.following.remove(tofollow)
        pro.save()
        message="you now do not follow "+name
        return JsonResponse({"message":message})
    else:
        return JsonResponse({"message":"You cannot unfollow yourself"})

def me(request):
    me=request.user.username
    pro=User.objects.get(username=me)
    email=pro.email
    posts=pro.profile.all()
    followers=pro.followers.all()
    following=pro.following.all()
    my_liked=pro.likers.all()
    return render(request,"network/profile.html",{
        "name":me,
        "email":email,
        "post":posts,
        "followers":followers,
        "following":following,
        "my_liked":my_liked
        })

@login_required
def like(request,usid):
    me=request.user.username
    pro=User.objects.get(username=me)
    post=Posts.objects.get(id=usid)
    post.likes+=1
    post.likedby.add(pro)
    post.save()
    return JsonResponse({"message":"Added to liked videos","likes":post.likes})

@login_required
def unlike(request,usid):
    me=request.user.username
    pro=User.objects.get(username=me)
    post=Posts.objects.get(id=usid)
    post.likes-=1
    post.likedby.remove(pro)
    post.save()
    return JsonResponse({"message":"Removed from liked videos","likes":post.likes})