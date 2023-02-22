
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.stroy.models import Category, SubCategory, Product, ProductImage, Size, Color
from apps.stroy.serializers import CategorySerializer, SubCategorySerializer, ProductSerializer, ProductImageSerializer, SizeSerializer, ColorSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['get'])
    def get_subcategories(self, request):
        category = self.get_object()
        queryset = SubCategory.objects.filter(category=category)
        serializer = SubCategorySerializer(queryset, many=True)
        pagination = self.paginate_queryset(queryset)
        if pagination is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def get_products(self, request):
        category = self.get_object()
        queryset = Product.objects.filter(category__category=category)
        serializer = ProductSerializer(queryset, many=True)
        pagination = self.paginate_queryset(queryset)
        if pagination is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['get'])
    def get_products(self, request):
        subcategory = self.get_object()
        queryset = Product.objects.filter(subcategory=subcategory)
        serializer = ProductSerializer(queryset, many=True)
        pagination = self.paginate_queryset(queryset)
        if pagination is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    