from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from apps.recommendation.models import (
    Recommendation,
    RecommendationProduct,
    RecommentationForCart,
    RecommendationForCartProduct,
    RecommendationForProductDetail,
    RecommendationForProductDetailProduct,
)
from apps.recommendation.serializers import (
    RecommendationSerializer,
    RecommendationProductSerializer,
    RecommentationForCartSerailizer,
    RecommendationForProductDetailProductSerializer,
    RecommendationForProductDetailSerializer,
)


class RecommendationViewSet(ReadOnlyModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer

    @action(methods=["get"], detail=True)
    def products(self, request, pk=None):
        queryset = RecommendationProduct.objects.filter(recommendation_id=pk)
        pagination = self.paginate_queryset(queryset)
        if pagination is not None:
            serializer = RecommendationProductSerializer(pagination, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = RecommendationProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecommentationForCartViewSet(viewsets.ViewSet):
    queryset = RecommentationForCart.objects.all()
    serializer_class = RecommentationForCartSerailizer

    def list(self, request):
        item = RecommentationForCart.objects.last()
        serializer = RecommentationForCartSerailizer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecommendationForProductDetailViewSet(ReadOnlyModelViewSet):
    queryset = RecommendationForProductDetail.objects.all()
    serializer_class = RecommendationForProductDetailSerializer

    @action(methods=["get"], detail=True)
    def products(self, request, pk=None):
        queryset = RecommendationForProductDetailProduct.objects.filter(
            recommendation_id=pk
        )
        pagination = self.paginate_queryset(queryset)
        if pagination is not None:
            serializer = RecommendationForProductDetailProductSerializer(
                pagination, many=True
            )
            return self.get_paginated_response(serializer.data)
        serializer = RecommendationForProductDetailProductSerializer(
            queryset, many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
