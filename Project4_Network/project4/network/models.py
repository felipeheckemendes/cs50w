from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    username = models.CharField(
        max_length=40, 
        primary_key=True,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9.-]{4,}$',
                message='Username should contain only letters, numbers, points (.) and dashes (-).',
                code='invalid_username'),
            RegexValidator(
                regex='^(login|logout|register|following)+$',
                message='Username not allowed, pertains to reserved list.',
                code='invalid_username',
                inverse_match=True)
        ]
    )
    following = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="followers")

class Post(models.Model):
    content = models.CharField(max_length=500)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add = True)
    updated_timestamp = models.DateTimeField(auto_now = True)
    likers = models.ManyToManyField(User, blank=True, related_name="liked_posts")

    def serialize(self, user):
        return {
            "id": self.pk,
            "content": self.content,
            "creator": self.creator.username,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "updated_timestamp": self.updated_timestamp.strftime("%b %d %Y, %I:%M %p"),
            "number_of_likes": self.likers.all().count(),
            "liked": user in self.likers.all(),
            "is_creator": user == self.creator,
        }

