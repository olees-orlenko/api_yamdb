from rest_framework import serializers

from reviews.models import Comment, Review, User


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = User


class UserSignUpSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_lenght=150)
    email = serializers.EmailField(required=True, max_lenght=150)

    class Meta:
        fields = ('email', 'username')
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_lenght=150)
    confirmation_code = serializers.CharField(required=True)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username'
                                          )
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username'
                                          )
    title = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('id',)
