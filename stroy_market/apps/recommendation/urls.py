from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.recommendation.views import (
    RecommendationViewSet,
    RecommentationForCartViewSet,
    RecommendationForProductDetailViewSet,
)

router = DefaultRouter()

router.register(
    "home-page-recommends", RecommendationViewSet, basename="recommendation"
)
router.register(
    "product-detail-recommends",
    RecommendationForProductDetailViewSet,
    basename="recommendation_for_product_detail",
)


urlpatterns = [
    path("", include(router.urls)),
    path(
        "cart/",
        RecommentationForCartViewSet.as_view({"get": "list"}),
        name="cart_recommendation",
    ),
]
