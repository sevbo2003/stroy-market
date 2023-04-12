from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.recommendation.views import RecommendationViewSet, RecommentationForCartViewSet

router = DefaultRouter()

router.register('home-page-recommends', RecommendationViewSet, basename='recommendation')
router.register('cart', RecommentationForCartViewSet, basename='recommendation-cart')


urlpatterns = [
    path('', include(router.urls)),
]
