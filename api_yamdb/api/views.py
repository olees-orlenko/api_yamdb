
from rest_framework import mixins
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from api.permissions import IsAdminOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django.core.exceptions import PermissionDenied
from reviews.models import Genre, Title, Category
from api.serializers import (
    GenreSerializer, TitleSerializer,
    CategorySerializer, TitleCreateSerializer)
from reviews.models import Genre, Title, Category
from api.serializers import (GenreSerializer,
                             TitleSerializer,
                             CategorySerializer)


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

    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def check_object_permissions(self, request, obj):
        if request.user.role == "admin":
            raise PermissionDenied()
        return super().check_object_permissions(request, obj)
