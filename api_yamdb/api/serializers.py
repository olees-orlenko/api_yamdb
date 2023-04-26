from rest_framework import serializers

from reviews.models import User

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
