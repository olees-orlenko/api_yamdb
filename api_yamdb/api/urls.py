from rest_framework.routers import DefaultRouter
from django.urls import include, path

from api.views import (TitleViewSet, GenreViewSet, CategoryViewSet,
                       CommentViewSet, ReviewViewSet, UserViewSet,
                       UserSignUpView, TokenView)

app_name = 'api'


router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', UserSignUpView.as_view(), name='signup'),
    path('v1/auth/token/', TokenView.as_view(), name='token'),
]
