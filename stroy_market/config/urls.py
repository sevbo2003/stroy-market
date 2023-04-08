from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from apps.authentication.views import PhoneTokenViewSet, UserViewSet


schema_view = get_schema_view(
    openapi.Info(
        title=settings.APP_NAME,
        default_version=f'v{settings.APP_VERSION}',
        description=settings.APP_DESCRIPTION,
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/auth/phone-token/', PhoneTokenViewSet.as_view({'post': 'create'}), name='phone_token'),
    path('api/v1/auth/phone-token/verify/', PhoneTokenViewSet.as_view({'post': 'verify'}), name='phone_token_verify'),
    path('api/v1/auth/user/', UserViewSet.as_view({'post': 'create'}), name='user'),
    path('api/v1/auth/user/me/', UserViewSet.as_view({'get': 'me'}), name='user_me'),
    path('api/v1/auth/user/reset-password/', UserViewSet.as_view({'post': 'reset_password'}), name='reset_password'),
    path('api/v1/stroy/', include("apps.stroy.urls")),
    path('api/v1/stroy/advertisement/', include("apps.advertisement.urls")),
    path('api/v1/stroy/recommendation/', include("apps.recommendation.urls")),
    path('api/v1/stroy/shipping/', include("apps.stroy.shipping.urls")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)