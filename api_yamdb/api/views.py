
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import filters
from rest_framework import status, viewsets

from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from api.permissions import IsAdminOrReadOnly

from django.core.exceptions import PermissionDenied
from reviews.models import Genre, Title, Category
from api.serializers import (
    GenreSerializer, TitleSerializer,
    CategorySerializer, TitleCreateSerializer,
    CommentSerializer, ReviewSerializer)
from reviews.models import Genre, Title, Category, Comment, Review
from api.serializers import (GenreSerializer,
                             TitleSerializer,
                             CategorySerializer)
from django.shortcuts import render


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterser_fields = ('category__slug', 'genre__slug', 'name', 'year')
    pagination_class = (LimitOffsetPagination,)
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleSerializer
        return TitleCreateSerializer


class GenreViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   mixins.ListModelMixin, viewsets.GenericViewSet,):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
    permission_classes = (IsAdminOrReadOnly)
    lookup_field = 'slug'


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    permission_classes = (IsAdminOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'



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

