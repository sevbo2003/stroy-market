from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

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
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)