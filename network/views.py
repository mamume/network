import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.http.response import Http404, HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, render
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


def edit(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post_id = data.get('id')
        edited_text = data.get('text')

        post = get_object_or_404(Post, pk=post_id)
        if post.owner == request.user:
            post.text = edited_text
            post.save()

            return JsonResponse({
                "text": post.text,
                "owner_id": post.owner.id,
                "owner_username": post.owner.username,
                "post_id": post.id,
                "created_at": post.created_at.strftime("%b. %d, %Y, %I:%M %P."),
                "likes_count": post.likes.count()
            })

        return HttpResponseNotAllowed("Not Allowed")

    return Http404("Not Found")


def like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    post.likes.add(request.user)
    post.save()

    return HttpResponse(post.likes.count())


def unlike(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    post.likes.remove(request.user)
    post.save()

    return HttpResponse(post.likes.count())
