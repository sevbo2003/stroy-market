from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.stroy.views import CategoryViewSet, SubCategoryViewSet, ProductViewSet, CartItemViewSet


router = DefaultRouter()

router.register("products", ProductViewSet)
router.register("categories", CategoryViewSet)
router.register("sub-categories", SubCategoryViewSet)
router.register("cart-items", CartItemViewSet, basename='cart-items')


urlpatterns = [
    path("", include(router.urls))
]