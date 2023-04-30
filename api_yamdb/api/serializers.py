from datetime import datetime

from django.db.models import Avg
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
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=150)


    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                f'Недопустипое имя - {value}!'
            )
        return value

    class Meta:
        fields = ('email', 'username')
        model = User

class TokenSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=True, max_length=150)
    confirmation_code = serializers.CharField(required=True)

    def validate_code(self, data):
        user = get_object_or_404(User, username=data['username'])
        if user.confirmation_code != data['confirmation_code']:
            raise serializers.ValidationError('Неверный код подтверждения')
        return RefreshToken.for_user(user).access_token 
    
    class Meta:
        fields = ('confirmation_code', 'username')
        model = User

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

    def validate(self, data):
        request = self.context['request']
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(
                    title=title,
                    author=request.user).exists():
                raise ValidationError(
                    'Допустимо не более 1 отзыва на произведение')
        return data
    
    def validate_score(self, score):
        if score < 1 or score > 10:
            raise serializers.ValidationError(
                'Рейтинг произведения должен быть от 1 до 10')
        return score

    class Meta:
        fields = '__all__'
        model = Review

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
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        current_year = datetime.today().year
        if value > current_year:
            raise serializers.ValidationError('Проверьте год выхода!')
        return value
    
    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score', default=0))
        return rating.get('score__avg')

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

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score', default=0))
        return rating.get('score__avg')
