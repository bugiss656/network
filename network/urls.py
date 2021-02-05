
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("newPost", views.newPost, name="newPost"),
    path("edit", views.editPost, name="editPost"),
    path("like", views.likePost, name="likePost"),
    path("profile/<str:user>", views.userProfile, name="userProfile"),
    path("follow", views.profileFollowing, name="profileFollowing"),
    path("followingPosts", views.followingUsersPosts, name="followingUsersPosts")
]
