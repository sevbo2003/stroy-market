from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.stroy.views import CategoryViewSet, SubCategoryViewSet, ProductViewSet, CartItemViewSet, ProductLikeViewSet, BestProductsViewSet, PopularProductsViewSet, NewsletterViewSets, RecommendedProductsViewSet


router = DefaultRouter()

router.register("products", ProductViewSet)
router.register("best-products", BestProductsViewSet)
router.register("popular-products", PopularProductsViewSet)
router.register("recommended-products", RecommendedProductsViewSet)
router.register("categories", CategoryViewSet)
router.register("sub-categories", SubCategoryViewSet)
router.register("cart-items", CartItemViewSet, basename='cart-items')
router.register("product-likes", ProductLikeViewSet, basename='product-likes')
router.register("newsletters", NewsletterViewSets, basename='newsletters')


urlpatterns = [
    path("", include(router.urls)),
    path("cart-items/", CartItemViewSet.as_view({"put": "update_cart",})),
]
