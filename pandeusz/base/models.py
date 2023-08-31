from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length = 200, null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Place(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank = True)
    # participants =
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    isPrivate = models.BooleanField(default=False)
    accessPassword = models.CharField(max_length=100, null=True, blank=True, default="")

    class Meta:
        ordering = ["updated", "created"]

    def __str__(self):
        return self.name

class Topic(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    files = models.ManyToManyField('File', related_name='topics')

    class Meta:
        ordering = ["name", "-created"]


class File(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    file = models.FileField(upload_to='post_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

