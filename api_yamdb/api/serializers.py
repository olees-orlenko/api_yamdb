from django.db.models import Avg

from datetime import datetime
from django.forms import ValidationError
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Genre, Title, Category, Comment, Review, User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=254,)
    username = serializers.RegexField(required=True, max_length=150,
                                      regex=r'^[\w.@+-]+$',)

    class Meta:
        fields = [
            'username',
            'email', 
            'bio',
            'first_name', 
            'last_name', 
            'role'
            ]
        model = User

class UserSignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=150) # исправила орфографическую ошибку в length
    email = serializers.EmailField(required=True, max_length=150) # и здесь


    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                f'Недопустипое имя - {value}!'
            )
        return value

    class Meta:
        fields = ('email', 'username')
        model = User

class TokenSerializer(serializers.ModelSerializer): # добавила Model, было serializers.Serializer

    username = serializers.CharField(required=True, max_length=150)
    confirmation_code = serializers.CharField(required=True)

    def validate_code(self, data):
        user = get_object_or_404(User, username=data['username'])
        if user.confirmation_code != data['confirmation_code']:
            raise serializers.ValidationError('Неверный код подтверждения')
        return RefreshToken.for_user(user).access_token 


class CommentSerializer(serializers.ModelSerializer):
    """ Сериализатор комментария."""
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username'
                                          )
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id',)


class ReviewSerializer(serializers.ModelSerializer):
    """ Сериализатор отзыва."""
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username'
                                          )
    title = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    """ Сериализатор категории."""
    class Meta:
        model = Category
        fields = 'slug', 'name'


class GenreSerializer(serializers.ModelSerializer):
    """ Сериализатор жанра."""
    class Meta:
        model = Genre
        fields = 'slug', 'name'


class TitleSerializer(serializers.ModelSerializer):
    """ Сериализатор произведения."""
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        current_year = datetime.today().year
        if value > current_year:
            raise serializers.ValidationError('Проверьте год выхода!')
        return value
    
    def get_avg_rating(self, obj):
        return obj.reviews.aggregate(rating=Avg('score'), default=0)

class TitleCreateSerializer(serializers.ModelSerializer):
    """ Сериализатор произведения."""
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug', many=True)
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug', many=False)

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        current_year = datetime.today().year
        if value > current_year:
            raise serializers.ValidationError('Проверьте год выхода!')
        return value

    def get_avg_rating(self, obj):
        return obj.reviews.aggregate(rating=Avg('score'), default=0)
