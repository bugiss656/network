from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.models import User

import json

from .forms import UserRegisterForm
from .models import *



def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        posts = Post.objects.all().order_by('-post_time')
        paginator = Paginator(posts, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'all_posts': page_obj
        }

        return render(request, "network/index.html", context)



def newPost(request):
    if request.method == 'POST':
        user = request.user
        post_body = request.POST['post-body']

        post = Post.objects.create(user=user, body=post_body)
        posts = Post.objects.all()

        return redirect('index')



def editPost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = json.loads(request.body)
            post_id = data['post_id']
            post_body = data['post']

            Post.objects.filter(id=post_id).update(body=post_body)

            return JsonResponse({'post_id': post_id, 'post_body': post_body}, safe=False)



def likePost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = json.loads(request.body)
            user = request.user
            action = data['action']
            post_id = data['post_id']

            post = Post.objects.get(id=post_id)

            if action == 'like':
                like = Likes.objects.create(user=user, post=post)

            elif action == 'unlike':
                like = Likes.objects.filter(user=user, post=post).delete()

            likes_counter = post.likes.all().count()

            return JsonResponse({'action': action, 'post_id': post_id, 'likes_counter': likes_counter}, safe=False)



def userProfile(request, user):
    user_profile = User.objects.get(username=user)
    logged_user = request.user

    user_profile_posts = Post.objects.filter(user=user_profile).order_by('-post_time')
    paginator = Paginator(user_profile_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    posts_count = user_profile_posts.count()

    followers = UserFollows.objects.filter(following_user=user_profile).count()
    follows = UserFollows.objects.filter(user=user_profile).count()
    do_follow = UserFollows.objects.filter(user=logged_user, following_user=user_profile)

    context = {
        'user': user_profile,
        'user_profile_posts': page_obj,
        'posts_count': posts_count,
        'followers': followers,
        'follows': follows,
        'user_follow': do_follow
    }

    return render(request, "network/profile.html", context)



def profileFollowing(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logged_user = request.user

        data = json.loads(request.body)
        action = data['action']
        user_profile = data['user_profile']

        if action == 'follow':
            follow = UserFollows.objects.create(user=logged_user, following_user=user_profile)
        elif action == 'unfollow':
            follow = UserFollows.objects.filter(user=logged_user, following_user=user_profile).delete()


        return JsonResponse({'action': action, 'profile': user_profile}, safe=False)


@login_required
def followingUsersPosts(request):
    if request.user.is_authenticated:
        logged_user = request.user

    following_users = list(UserFollows.objects.filter(user=logged_user).values_list('following_user', flat=True))
    following_users_posts = Post.objects.filter(user__username__in=following_users).order_by('-post_time')

    paginator = Paginator(following_users_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'following_users': following_users,
        'following_users_posts': page_obj
    }

    return render(request, "network/following.html", context)



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
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')

            return redirect('login')

    else:
        form = UserRegisterForm()

    return render(request, 'network/register.html', {'form': form})
