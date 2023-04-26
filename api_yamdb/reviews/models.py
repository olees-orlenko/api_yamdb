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

    username = models.CharField(
        'Логин',
        unique=True,
        blank=False,
        max_length=150,
    )
    email = models.EmailField(
        'e-mail адрес',
        unique=True,
        blank=False,
        max_length=50,
    )
    first_name = models.CharField(
        'Имя',
        blank=False,
        max_length=150,
    )
    last_name = models.CharField(
        'Фамилия',
        blank=True,
        max_length=150,
    )
    bio = models.TextField(
        'О пользователе',
        blank=True,
    )
    role = models.CharField(
        choices=ROLE_CHOICES,
        default='user'
    )
    
    @property
    def is_admin(self):
        return self.role == self.ADMIN
    
    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
    
    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username
    