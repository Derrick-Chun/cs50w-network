from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.db.models import F, Q


class User(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    liked_by = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.author.username}: {self.content[:30]}"

    @property
    def likes_count(self):
        return self.liked_by.count()


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"], name="unique_follow_pair"
            ),
            models.CheckConstraint(
                check=~Q(follower=F("following")),
                name="no_self_follow",
            ),
        ]

    def __str__(self):
        return f"{self.follower.username} → {self.following.username}"
