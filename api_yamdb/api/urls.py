from rest_framework.routers import DefaultRouter
from django.urls import include, path
from api.views import TitleViewSet, GenreViewSet, CategoryViewSet, CommentViewSet, ReviewViewSet

app_name = 'api'


router = DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.jwt')),

]