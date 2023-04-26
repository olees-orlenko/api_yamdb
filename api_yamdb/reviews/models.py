from django.conf import settings
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
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


# class User(models.Model):
#     username = models.CharField(max_length=150, unique=True)
#     email = models.EmailField(max_length=254, unique=True)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     bio = models.TextField(blank=True)
#     ROLE_CHOICES = [("user", "user"),
#                     ("moderator", "moderator"),
#                     ("admin", "admin")]
#     role = models.CharField(max_length=9, choices=ROLE_CHOICES)

#     class Meta:
#         ordering = ["username"]

#     def __str__(self):
#         return self.username


class Title(models.Model):
    name = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    description = models.TextField('Описание',)
    year = models.IntegerField()
    rating = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-year', 'name']
        indexes = [
            models.Index(fields=['name',
                                 'category',
                                 'genre',
                                 'year'],
                         name='title_index'), ]


class Review(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews')
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews')
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    text = models.TextField('Текст отзыва')
    pub_date = models.DateTimeField('Дата добавления',
                                    auto_now_add=True,
                                    db_index=True)

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
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
