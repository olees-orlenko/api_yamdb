from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title, User


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'category',
                    'genre',
                    'description',
                    'year',
                    'rating'
                    )
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'review', 'text', 'pub_date')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'text', 'title', 'score', 'pub_date')


admin.site.register(User)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)

