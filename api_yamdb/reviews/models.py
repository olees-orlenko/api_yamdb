from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLE_CHOICES =  [
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR),
        (USER, USER),
    ]

    username = models.CharField()
    email = models.EmailField()
    first_name = models.CharField()
    last_name = models.CharField()
    bio = models.TextField()
    role = models.CharField()