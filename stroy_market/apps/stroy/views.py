from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.stroy.models import Category, SubCategory, Product, CartItem, ProductLike, BestProduct, PopularProduct
from apps.stroy.serializers import CategorySerializer, SubCategorySerializer, ProductSerializer, ProductCommentSerializer, CommentLikeSerializer, CartItemSerializer, ProductLikeSerializer, BestProductSerializer, PopularProductSerializer
from apps.stroy.filters import ProductFilter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get', 'head', 'options']
    lookup_field = 'slug'

    @action(detail=True, methods=['get'])
    def get_subcategories(self, request, slug=None):
        category = self.get_object()
        queryset = category.subcategory_set.all()
        serializer = SubCategorySerializer(queryset, many=True)
        pagination = self.paginate_queryset(queryset)
        if pagination is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def get_products(self, request, slug=None):
        instance = self.get_object()
        queryset = Product.objects.filter(category__category__slug=slug)
        serializer = ProductSerializer(queryset, many=True)
        pagination = self.paginate_queryset(queryset)
        if pagination is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [permissions.IsAdminUser]
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
    
    def get_permissions(self):
        if self.action in ['list', 'get_products', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


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

    @action(detail=True, methods=['post'])
    def dislike_comment(self, request, pk=None):
        serializer = CommentLikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, dislike=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CartItemViewSet(viewsets.ViewSet):
    def list(self, request):
        if request.user.is_authenticated:
            queryset = CartItem.objects.filter(user=request.user)
        else:
            queryset = CartItem.objects.filter(session_key=request.session.session_key)
        serializer = CartItemSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        if request.user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                product_id=product_id,
            )
        else:
            cart_item, created = CartItem.objects.get_or_create(
                session_key=request.session.session_key,
                product_id=product_id,
            )
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()

        serializer = CartItemSerializer(cart_item, context={'request': request})

        return Response(serializer.data)

    @action(detail=False, methods=['delete'])
    def clear(self, request):
        if request.user.is_authenticated:
            queryset = CartItem.objects.filter(user=request.user)
        else:
            queryset = CartItem.objects.filter(session_key=request.session.session_key)
        queryset.delete()
        return Response(status=204)


class ProductLikeViewSet(viewsets.ViewSet):
    def create(self, request):
        product_id = request.data.get('product_id')
        product = Product.objects.get(id=product_id)
        if request.user.is_authenticated:
            product_like, created = ProductLike.objects.get_or_create(
                user=request.user,
                product=product
            )
        else:
            product_like, created = ProductLike.objects.get_or_create(
                session_key=request.session.session_key,
                product=product
            )
        if not created:
            product_like.delete()
        else:
            product_like.save()
        return Response(status=status.HTTP_200_OK)
    
    def list(self, request):
        if request.user.is_authenticated:
            queryset = ProductLike.objects.filter(user=request.user)
        else:
            queryset = ProductLike.objects.filter(session_key=request.session.session_key)
        serializer = ProductLikeSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'])
    def clear(self, request):
        if request.user.is_authenticated:
            queryset = ProductLike.objects.filter(user=request.user)
        else:
            queryset = ProductLike.objects.filter(session_key=request.session.session_key)
        queryset.delete()
        return Response(status=204)


class BestProductsViewSet(viewsets.ModelViewSet):
    queryset = BestProduct.objects.all()
    serializer_class = BestProductSerializer
    http_method_names = ['get', 'head', 'options']


class PopularProductsViewSet(viewsets.ModelViewSet):
    queryset = PopularProduct.objects.all()
    serializer_class = PopularProductSerializer
    http_method_names = ['get', 'head', 'options']
