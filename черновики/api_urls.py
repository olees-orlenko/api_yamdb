import rest_framework
from rest_framework.routers import DefaultRouter
from django.urls import include, path
from черновики.api_views import TitleViewSet, ReviewViewSet, CommentViewSet

app_name = 'api'


router = DefaultRouter()
router.register(r'title', TitleViewSet, basename='title')
router.register(r'review', ReviewViewSet, basename='review')
router.register(r'gerne', , basename='gerne')
router.register(r'category', , basename='category')
router.register(
    r'review/(?P<review_id>\d+)/comments', CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
