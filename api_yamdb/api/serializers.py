from datetime import datetime

from django.db.models import Avg
from django.forms import ValidationError
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Genre, Title, Category, Comment, Review, User
from .validators import validate_username


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True, 
        max_length=150, 
        validators=[
            validate_username,
            # UniqueValidator(queryset=User.objects.all())
        ],
        )
    email = serializers.EmailField(
        required=True, 
        max_length=254,
        # validators=[UniqueValidator(queryset=User.objects.all())]
        )

    class Meta:
        model = User
        fields = (
            'username',
            'email', 
            'first_name', 
            'last_name', 
            'bio',
            'role'
            )


class UserSignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True, 
        max_length=150, 
        validators=[
            validate_username,
            UniqueValidator(queryset=User.objects.all())
        ],
        )
    email = serializers.EmailField(
        required=True, 
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )

    class Meta:
        model = User
        fields = ('email', 'username')

        
class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True, 
        max_length=150, 
        validators=[validate_username]
        )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('confirmation_code', 'username')


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
