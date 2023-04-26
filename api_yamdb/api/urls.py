from rest_framework.routers import DefaultRouter
from django.urls import include, path
from api.views import TitleViewSet, GenreViewSet, CategoryViewSet

app_name = 'api'


router = DefaultRouter()
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'categories', CategoryViewSet, basename='categories')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
