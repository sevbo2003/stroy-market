from django.urls import path, include
from .views import BannerViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'banners', BannerViewSet, basename='banners')


urlpatterns = [
    path('', include(router.urls)),
]