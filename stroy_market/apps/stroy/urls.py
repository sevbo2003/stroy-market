from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.stroy.views import CategoryViewSet, SubCategoryViewSet, ProductViewSet


router = DefaultRouter()

router.register("products", ProductViewSet)
router.register("categories", CategoryViewSet)
router.register("sub-categories", SubCategoryViewSet)


urlpatterns = [
    path("", include(router.urls))
]