
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.stroy.models import Category, SubCategory, Product, ProductImage, Size, Color, ProductComment, CommentLike
from apps.stroy.serializers import CategorySerializer, SubCategorySerializer, ProductSerializer, ProductImageSerializer, ProductCommentSerializer, CommentLikeSerializer
from apps.stroy.filters import ProductFilter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    @action(detail=True, methods=['get'])
    def get_subcategories(self, request):
        category = self.get_object()
        queryset = category.subcategory_set.all()
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
    lookup_field = 'slug'

    @action(detail=True, methods=['get'])
    def get_products(self, request):
        subcategory = self.get_object()
        queryset = subcategory.product_set.all()
        serializer = ProductSerializer(queryset, many=True)
        pagination = self.paginate_queryset(queryset)
        if pagination is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    http_method_names = ['post', 'get', 'head', 'options']

    def retrieve(self, request, *args, **kwargs):
        saved_products = request.session.get('saved_products', [])
        instance = self.get_object()
        if instance.id not in saved_products:
            instance.views += 1
            instance.save()
            saved_products.append(instance.id)
            request.session['saved_products'] = saved_products
        serializer = self.get_serializer(instance)
        product_data = serializer.data
        similar_products = Product.objects.filter(category=instance.category).exclude(id=instance.id)[:6]
        you_may_like = Product.objects.filter(category__category=instance.category.category).exclude(id=instance.id).order_by('-created_at')[:6]
        similar_products_data = ProductSerializer(similar_products, many=True).data
        you_may_like_data = ProductSerializer(you_may_like, many=True).data
        return Response(
            {
                "product": product_data,
                "similar_products": similar_products_data,
                "you_may_like": you_may_like_data
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        serializer = ProductCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, product_id=pk)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def get_comments(self, request, pk=None):
        product = self.get_object()
        queryset = product.productcomment_set.all()
        serializer = ProductCommentSerializer(queryset, many=True)
        pagination = self.paginate_queryset(queryset)
        if pagination is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def like_comment(self, request, pk=None):
        serializer = CommentLikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, like=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    