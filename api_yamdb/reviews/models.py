from django.db import models



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
