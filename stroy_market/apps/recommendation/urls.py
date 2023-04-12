from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.recommendation.views import RecommendationViewSet, RecommentationForCartViewSet

router = DefaultRouter()

router.register('home-page-recommends', RecommendationViewSet, basename='recommendation')


urlpatterns = [
    path('', include(router.urls)),
    path('cart/', RecommentationForCartViewSet.as_view({'get': 'list'}), name='cart_recommendation'),
]
