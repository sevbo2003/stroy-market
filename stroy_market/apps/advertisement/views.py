from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Banner
from .serializers import BannerSerializer


class BannerViewSet(ReadOnlyModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Banner.objects.filter(is_active=True)
    