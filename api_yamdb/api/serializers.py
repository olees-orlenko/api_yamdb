from datetime import datetime

from django.db.models import Avg
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from django.core.validators import validate_email

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from reviews.models import Genre, Title, Category, Comment, Review, User
#from .validators import validate_username


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+$', required=True, max_length=50)
    email = serializers.EmailField(required=True, max_length=254)
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Такое имя использовать запрещено')
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Этот емэйл уже занят')
        return value
        
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
    email = serializers.EmailField(required=True, max_length=50)
    username = serializers.RegexField(regex=r'^[\w.@+-]+$', required=True, max_length=50)
    
    class Meta:
        model = User
        fields = ('username', 'email')
    
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Такое имя использовать запрещено')
        return value


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True, 
        max_length=150
        )
    confirmation_code = serializers.CharField(required=True)

    def validate_code(self, data):
        user = get_object_or_404(User, username=data['username'])
        if user.confirmation_code != data['confirmation_code']:
            raise serializers.ValidationError('Неверный код подтверждения')
        return RefreshToken.for_user(user).access_token 
    
    class Meta:
        fields = ('confirmation_code', 'username')
        model = User

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
                    'Вы можете оставить только 1 отзыв на произведение')
        return data
    
    def validate_score(self, score):
        if 1 > score > 10:
            raise serializers.ValidationError(
                'Оценка должна быть от 1 до 10')
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
