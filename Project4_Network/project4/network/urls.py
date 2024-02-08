
from django.urls import path

from . import views

urlpatterns = [
    # Views
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<str:user_id>", views.user_view, name="user_view"),
    path("following", views.following_view, name="following_view"),

    # API Calls
    path("get_posts", views.get_posts, name="get_posts"),
    path("create_post", views.create_post, name="create_post"),
    path("edit_post", views.edit_post, name="edit_post"),
    path("like_post/<int:post_id>", views.like_post, name="like_post"),
    path("follow", views.follow, name="follow")
]
