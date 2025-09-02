from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # auth
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # posts
    path("posts", views.create_post, name="create_post"),  # POST only
    path("posts/<int:post_id>/edit", views.edit_post, name="edit_post"),
    path("posts/<int:post_id>/like", views.toggle_like, name="toggle_like"),

    # profiles & following
    path("users/<str:username>", views.profile, name="profile"),
    path("users/<str:username>/follow", views.toggle_follow, name="toggle_follow"),
    path("following", views.following, name="following"),
]
