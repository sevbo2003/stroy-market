from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.stroy.shipping.views import OrderViewSet, OrderAddressViewSet, CheckPromocodeViewSet


router = DefaultRouter()

router.register("orders", OrderViewSet)
router.register("order-addresses", OrderAddressViewSet)
router.register("check-promocode", CheckPromocodeViewSet)


urlpatterns = [
    path("", include(router.urls))
]