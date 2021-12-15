from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import Post, User


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", context={
        'page_obj': page_obj
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


def create_post(request):
    if request.method == "POST":
        post_text = request.POST.get("post")
        message = ""

        if post_text == "":
            message = "Cannot create empty post"
        else:
            try:
                post = Post.objects.create(text=post_text, owner=request.user)
                post.save()
                return HttpResponseRedirect(reverse("index"))
            except Exception as e:
                message = e

        return render(request, "network/index.html", context={
            "message": message
        })


def profile(request, id):
    user = User.objects.get(pk=id)
    following_count = User.objects.filter(followers__id=id).count()

    isLoggedUserProfile = id == request.user.id

    followed = False
    if not isLoggedUserProfile:
        followed = User.objects.get(pk=id).followers.filter(id=request.user.id)

    # Get User Posts
    posts = Post.objects.filter(owner__id=id)

    return render(request, 'network/profile.html', context={
        "profile_user": user,
        "following_count": following_count,
        "posts": posts,
        "isLoggedUserProfile": isLoggedUserProfile,
        "followed": followed
    })


def follow(request, id):
    user = User.objects.get(pk=id)
    user.followers.add(request.user)

    return HttpResponseRedirect(f'/profile/{id}')


def unfollow(request, id):
    user = User.objects.get(pk=id)
    user.followers.remove(request.user)

    return HttpResponseRedirect(f'/profile/{id}')


def following(request):
    followed_users = User.objects.filter(followers__id=request.user.id)
    posts = Post.objects.filter(owner__in=followed_users)
    print(posts)

    return render(request, 'network/following.html', context={
        'posts': posts
    })
