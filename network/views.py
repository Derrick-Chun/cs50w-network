import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotAllowed,
)
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import User, Post, Follow


# ---------- Core pages ----------

def index(request):
    """All posts, newest first, paginated."""
    posts = Post.objects.select_related("author")
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "network/index.html", {"page_obj": page_obj})


@login_required
@require_POST
def create_post(request):
    """Create a new post (form POST from index)."""
    content = (request.POST.get("content") or "").strip()
    if content:
        Post.objects.create(author=request.user, content=content)
    return redirect("index")


# ---------- Authentication (from distribution, kept simple) ----------

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return redirect("index")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except Exception as exc:
            return render(request, "network/register.html", {
                "message": f"Registration error: {exc}"
            })
        login(request, user)
        return redirect("index")
    else:
        return render(request, "network/register.html")


# ---------- Profiles & following ----------

def profile(request, username):
    """Show a user's profile with their posts."""
    profile_user = get_object_or_404(User, username=username)

    is_own_profile = request.user.is_authenticated and request.user == profile_user
    is_following = False
    if request.user.is_authenticated and not is_own_profile:
        is_following = Follow.objects.filter(
            follower=request.user, following=profile_user
        ).exists()

    followers_count = profile_user.followers.count()
    following_count = profile_user.following.count()

    posts = Post.objects.filter(author=profile_user).select_related("author")
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "network/profile.html",
        {
            "profile_user": profile_user,
            "is_own_profile": is_own_profile,
            "is_following": is_following,
            "followers_count": followers_count,
            "following_count": following_count,
            "page_obj": page_obj,
        },
    )


@login_required
@require_POST
def toggle_follow(request, username):
    """Follow/unfollow another user (never yourself)."""
    target = get_object_or_404(User, username=username)
    if target == request.user:
        return HttpResponseForbidden("You cannot follow yourself.")

    # Toggle
    obj, created = Follow.objects.get_or_create(
        follower=request.user, following=target
    )
    if not created:
        obj.delete()
        now_following = False
    else:
        now_following = True

    # JSON for AJAX callers, or redirect for normal form
    if request.headers.get("Accept") == "application/json":
        return JsonResponse(
            {
                "following": now_following,
                "followers_count": target.followers.count(),
            }
        )
    return redirect("profile", username=target.username)


@login_required
def following(request):
    """Feed of posts from users the current user follows."""
    followed_users = User.objects.filter(followers__follower=request.user)
    posts = Post.objects.filter(author__in=followed_users).select_related("author")
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "network/following.html", {"page_obj": page_obj})


# ---------- AJAX: edit post & like/unlike ----------

@login_required
@require_POST
def edit_post(request, post_id):
    """
    Edit your own post via fetch() POST containing JSON body: {"content": "..."}
    Returns JSON with updated content and a simple timestamp string.
    """
    post = get_object_or_404(Post, pk=post_id)

    if post.author != request.user:
        return HttpResponseForbidden("You can only edit your own posts.")

    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON.")

    content = (data.get("content") or "").strip()
    if not content:
        return HttpResponseBadRequest("Content cannot be empty.")

    post.content = content
    post.save(update_fields=["content", "timestamp"])  # timestamp stays as created time

    return JsonResponse(
        {
            "ok": True,
            "id": post.id,
            "content": post.content,
            "likes_count": post.likes_count,
            "timestamp": post.timestamp.strftime("%Y-%m-%d %H:%M"),
        }
    )


@login_required
@require_POST
def toggle_like(request, post_id):
    """
    Toggle like/unlike for the given post. Expects POST with CSRF token.
    Returns JSON: {"liked": bool, "likes_count": int}
    """
    post = get_object_or_404(Post, pk=post_id)

    if request.user in post.liked_by.all():
        post.liked_by.remove(request.user)
        liked = False
    else:
        post.liked_by.add(request.user)
        liked = True

    return JsonResponse({"liked": liked, "likes_count": post.likes_count})
