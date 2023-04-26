from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


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
        default='user',
        max_length=10,
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

class Category(models.Model):

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['name']


class Genre(models.Model):

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'
        ordering = ['name']


class Title(models.Model):

    name = models.CharField(max_length=250, help_text='Название произведения')
    categories = models.ForeignKey(
        Category, verbose_name='Slug категории',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )
    genre = models.ManyToManyField(
        Genre, verbose_name='Slug жанра'
    )
    description = models.TextField('Описание', blank=True)
    year = models.PositiveIntegerField(help_text='Год выхода произведения')
    rating = models.PositiveIntegerField(null=True, default=None)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-year',)
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'categories'],
                name='unique_name_categories'
            )
        ]

class Comment(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments')
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               null=True,
                               blank=True)
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField('Дата добавления',
                                    auto_now_add=True,
                                    db_index=True)

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ('-pub_date',)
