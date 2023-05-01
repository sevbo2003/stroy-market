from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from apps.stroy.models import Product
from apps.stroy.filters import ProductFilter
from apps.recommendation.models import (
    Recommendation,
    RecommendationProduct,
    RecommentationForCart,
    RecommendationForCartProduct,
    RecommendationForProductDetail,
    RecommendationForProductDetailProduct,
    RecommendationForCategory,
    RecommendationForCategoryProduct,
)
from apps.recommendation.serializers import (
    RecommendationSerializer,
    RecommendationProductSerializer,
    RecommentationForCartSerailizer,
    RecommendationForProductDetailProductSerializer,
    RecommendationForProductDetailSerializer,
    RecommendationForCategorySerializer,
    RecommendationForCategoryProductSerializer,
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

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=["get"], detail=True)
    def products(self, request, pk=None):
        id = Product.objects.get(pk=pk)
        queryset = RecommendationForProductDetail.objects.filter(product_id=id).order_by("-id")
        pagination = self.paginate_queryset(queryset)
        if pagination is not None:
            serializer = RecommendationForProductDetailSerializer(pagination, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = RecommendationForProductDetailProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecommendationForCategoryViewSet(ReadOnlyModelViewSet):
    queryset = RecommendationForCategory.objects.all()
    serializer_class = RecommendationForCategorySerializer

    def list(self, request):
        category_id = request.query_params.get("category_id")
        if category_id:
            queryset = RecommendationForCategory.objects.filter(category_id=category_id)
        else:
            queryset = RecommendationForCategory.objects.all()
        pagination = self.paginate_queryset(queryset)
        if pagination is not None:
            serializer = RecommendationForCategorySerializer(pagination, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = RecommendationForCategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=True)
    def products(self, request, pk=None):
        queryset = RecommendationForCategoryProduct.objects.filter(recommendation_id=pk)
        pagination = self.paginate_queryset(queryset)
        if pagination is not None:
            serializer = RecommendationForCategoryProductSerializer(
                pagination, many=True
            )
            return self.get_paginated_response(serializer.data)
        serializer = RecommendationForCategoryProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
