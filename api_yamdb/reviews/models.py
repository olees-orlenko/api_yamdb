from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


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


class User(models.Model):

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    ROLE_CHOICES = [("user", "user"), ("moderator", "moderator"), ("admin", "admin")]
    role = models.CharField(max_length=9, choices=ROLE_CHOICES)

    class Meta: 
        ordering = ["username"]

    def __str__(self):
        return self.username


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


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.PositiveSmallIntegerField('Оценка', validators=[
            MaxValueValidator(10),
            MinValueValidator(1),
    ])
    text = models.TextField('Текст отзыва')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    def str(self):
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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True, db_index=True)

    def str(self):
        return self.text[:15]

    class Meta:
        ordering = ('-pub_date',)
