from rest_framework import filters, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError

from reviews.models import Comment, Review, Title, User
from api.serializers import (
    CommentSerializer, ReviewSerializer,
    UserSerializer, TokenSerializer, UserSignUpSerializer) 


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']   
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_class = []
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,) 
    search_fields = ('username',)


class UserSignUpView(APIView):
    def user_signup(request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        try:
            user, _ = User.objects.get_or_create(
                username=username, 
                email=email
            )
        except IntegrityError:
            raise ValidationError(
                'Имя пользователя или email уже используются',
                status.HTTP_400_BAD_REQUEST
            )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Подтверждение регистрации.',
            message=f'Код подтверждения: {confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_title(self):
        self.title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return self.title

    def get_queryset(self):
        title = self.get_title()
        new_queryset = title.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=self.request.user, title=title)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
