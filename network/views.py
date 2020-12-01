from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse

from .models import User, Posts, Image
from .forms import Postform

import os

def index(request):
    po = Posts.objects.all().order_by('-timestamp').reverse()
    post = po.reverse()

    my_liked=[]
    if request.user.is_authenticated:
        me=request.user.username
        person=User.objects.get(username=me)
        my_liked=person.likers.all()
    p=Paginator(post,10) #Paginate to get 10 posts at a time
    if request.GET.get('page'):
        pgn=request.GET.get('page')
        if (int(pgn)<=p.num_pages):
            send=p.page(pgn)
        else:
            send=p.page(1)
    else:
        send=p.page(1)

    #To include the images with the posts
    album=[]
    for thing in send:
        pics=thing.pics.all()
        album.append(pics)

    return render(request, "network/index.html",{
        'post':send,
        'num':p.num_pages,
        'my_liked':my_liked,
        'album':album
    })

def all_posts(request):
    po = Posts.objects.all().order_by('-timestamp').reverse()
    post = po.reverse()

    #Paginate to get 10 posts at a time
    p=Paginator(post,10) 
    send=p.page(1)


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


#The primary post creation function
def upload(request):
    if request.method == "POST":
        me = request.user.username
        creator = User.objects.get(username=me)
        content=request.POST['content']

        #Trying to create a post
        create_post = Posts.objects.create(creator=creator,content=content)
        create_post.save()
        try:
            uploaded_image = request.FILES['image']
            fs=FileSystemStorage()
            filename=fs.save(uploaded_image.name,uploaded_image)
            uploaded_file_url=fs.url(filename)
            store_image= Image.objects.create(uploader=creator,post=create_post,link=uploaded_file_url)
            store_image.save()

        except Exception:
            pass

        return HttpResponseRedirect(reverse("index"))

    elif request.method == "GET":
        form = Postform()
        return render(request,"network/create.html",{
            "form":form
            })

    else:
        return HttpResponse('error')

#To display individual post
def post(request,psid):
    me=request.user.username
    person=User.objects.get(username=me)
    post=Posts.objects.get(id=psid)
    my_liked=person.likers.all()
    album=post.pics.all()
    return render(request,"network/post.html",{
        "post":post,
        "my_liked":my_liked,
        "album":album
        })

#To display individual profile
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

    p=Paginator(posts,10) #Paginate to get 10 posts at a time
    if request.GET.get('page'):
        pgn=request.GET.get('page')
        if (int(pgn)<=p.num_pages):
            send=p.page(pgn)
        else:
            send=p.page(1)
    else:
        send=p.page(1)

    album=[]
    for thing in send:
        pics=thing.pics.all()
        album.append(pics)

    return render(request,"network/profile.html",{
        "me":person,
        "profile":pro,
        "name":name,
        "email":email,
        "post":send,
        "num":p.num_pages,
        "followers":followers,
        "following":following,
        "my_liked":my_liked,
        "my_following":my_following,
        "album":album
        })

@login_required
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

    p=Paginator(basket,10) #Paginate to get 10 posts at a time
    if request.GET.get('page'):
        pgn=request.GET.get('page')
        if (int(pgn)<=p.num_pages):
            send=p.page(pgn)
        else:
            send=p.page(1)
    else:
        send=p.page(1)

    album=[]
    for thing in send:
        pics=thing.pics.all()
        album.append(pics)

    return render(request,"network/index.html",{
        'post':reversed(send),
        'num':p.num_pages,
        'my_liked':my_liked,
        "album":album
        })

#Functions for API requests

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
def like(request,psid):
    me=request.user.username
    pro=User.objects.get(username=me)
    post=Posts.objects.get(id=psid)
    post.likes+=1
    post.likedby.add(pro)
    post.save()
    return JsonResponse({"message":"Added to liked videos","likes":post.likes})

@login_required
def unlike(request,psid):
    me=request.user.username
    pro=User.objects.get(username=me)
    post=Posts.objects.get(id=psid)
    post.likes-=1
    post.likedby.remove(pro)
    post.save()
    return JsonResponse({"message":"Removed from liked videos","likes":post.likes})


@login_required
def edit(request):
    if request.method == "POST":
        content = request.POST['content']
        print(content)
        me = request.user.username
        creator = User.objects.get(username=me)
        print (creator)
        the_id = request.POST['content']
        print(the_id)

        #Trying to create a post
        create_post,c = Posts.objects.update_or_create(creator=creator, content= content)
        create_post.save()

        try:
            uploaded_image=request.FILES['image']
            fs=FileSystemStorage()
            filename=fs.save(uploaded_image.name,uploaded_image)
            uploaded_file_url=fs.url(filename)
            store_image= Image.objects.create(uploader=creator,post=create_post,link=uploaded_file_url)
            store_image.save()

        except Exception:
            pass

        #Exception handling for failed post creation

        return HttpResponseRedirect(reverse("index"))

    elif request.method=="GET":
        me=request.user.username
        pro=User.objects.get(username=me)
        psid=request.GET['psid']
        post=Posts.objects.get(id=psid)

        try:
            pic=Image.objects.get(post=post)
        except:
            pic=None

        if (post.creator == pro):
            return render(request,"network/edit.html",{
                "profile":pro,
                "post":post,
                "pic":pic
            })
        else:
            return HttpResponseRedirect(reverse("index"))

    else:
        raise Http404



@login_required
def delete(request,psid):
    if request.method=="GET":
        me=request.user.username
        pro=User.objects.get(username=me)
        post=Posts.objects.get(id=psid)
        if (post.creator == pro):
            pics=Image.objects.filter(post=post)
            for pic in pics:
                if os.path.exists(pic.link):
                    os.remove(pic.link)
            post.delete()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("index"))