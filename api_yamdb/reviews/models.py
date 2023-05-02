from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from api.validators import validate_score, validate_username, validate_year

USERNAME_LENGTH = 150
EMAIL_LENGTH = 254
SLUG_LENGTH = 50
ART_LENGTH = 256


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLE_CHOICES = [
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR),
        (USER, USER),
    ]

    username = models.CharField(
        'Логин',
        unique=True,
        blank=False,
        null=False,
        max_length=USERNAME_LENGTH,
        validators=(validate_username,)
    )
    email = models.EmailField(
        'e-mail адрес',
        unique=True,
        blank=False,
        max_length=EMAIL_LENGTH
    )
    first_name = models.CharField(
        'Имя',
        blank=True,
        null=True,
        max_length=USERNAME_LENGTH
    )
    last_name = models.CharField(
        'Фамилия',
        blank=True,
        null=True,
        max_length=USERNAME_LENGTH
    )
    bio = models.TextField(
        'О пользователе',
        blank=True,
        null=True,
        max_length=USERNAME_LENGTH
    )
    role = models.CharField('Роль',
                            choices=ROLE_CHOICES,
                            default=USER,
                            max_length=max([len(role[1])
                                            for role in ROLE_CHOICES]))
    confirmation_code = models.CharField('Код подтверждения',
                                         blank=False,
                                         null=True,
                                         max_length=USERNAME_LENGTH,
                                         default='XXXX')

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username')
        ]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return (self.role == self.ADMIN or self.is_superuser)

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER


class CommonDataAbstractModel(models.Model):
    class Meta:
        abstract = True

    name = models.CharField('Название', max_length=ART_LENGTH)
    slug = models.SlugField('Идентификатор',
                            max_length=SLUG_LENGTH,
                            unique=True)


class Category(CommonDataAbstractModel):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} {self.slug}'

    def get_absolute_url(self):
        return reverse('category_detail', args=[str(self.slug)])


class Genre(CommonDataAbstractModel):

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('id', 'name')

    def __str__(self):
        return self.name


class Title(models.Model):

    name = models.CharField(
        max_length=ART_LENGTH,
        help_text='Название произведения'
    )
    year = models.PositiveIntegerField(
        help_text='Год выхода произведения',
        validators=[validate_year]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанр'
    )
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year',)
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category'],
                name='unique_name_category'
            )
        ]

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews',
                               verbose_name='Автор')
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews',
                              verbose_name='Произведение')
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[validate_score,
                    MaxValueValidator(10),
                    MinValueValidator(1)]
    )
    text = models.TextField('Текст отзыва')
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]

    def __str__(self):
        return f'{self.title}, {self.author}, {self.score}'


class Comment(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Автор')
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               null=True,
                               blank=True,
                               verbose_name='Отзыв')
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]
