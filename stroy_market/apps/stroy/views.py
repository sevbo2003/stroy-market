from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.stroy.models import (
    Category,
    SubCategory,
    Product,
    CartItem,
    ProductLike,
    Newsletter,
    Question,
    Answer,
)
from apps.stroy.serializers import (
    CategorySerializer,
    SubCategorySerializer,
    ProductSerializer,
    ProductCommentSerializer,
    CommentLikeSerializer,
    CartItemSerializer,
    ProductLikeSerializer,
    NewsletterSerializer,
    QuestionSerializer,
    AnswerSerializer,
    CommentDislikeSerializer
)
from apps.stroy.filters import ProductFilter
from apps.recommendation.models import SpecialOffer
from apps.recommendation.serializers import SpecialOfferSerializer
from django.db.models import F, Sum


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ["get", "head", "options"]
    lookup_field = "slug"

    @action(detail=True, methods=["get"])
    def get_subcategories(self, request, slug=None):
        category = self.get_object()
        queryset = category.subcategory_set.all()
        serializer = SubCategorySerializer(queryset, many=True)
        pagination = self.paginate_queryset(queryset)
        if pagination is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def get_special_offers(self, request, slug=None):
        category = self.get_object()
        queryset = SpecialOffer.objects.filter(category=category)
        serializer = SpecialOfferSerializer(queryset, many=True)
        pagination = self.paginate_queryset(queryset)
        if pagination is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
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
    http_method_names = ["get", "head", "options"]
    lookup_field = "slug"

    @action(detail=True, methods=["get"])
    def get_products(self, request, slug=None):
        subcategory = self.get_object()
        queryset = subcategory.product_set.all()
        serializer = ProductSerializer(queryset, many=True)
        pagination = self.paginate_queryset(queryset)
        if pagination is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action in ["list", "get_products", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    http_method_names = ["post", "get", "head", "options"]

    def retrieve(self, request, *args, **kwargs):
        saved_products = request.session.get("saved_products", [])
        instance = self.get_object()
        if instance.id not in saved_products:
            instance.views += 1
            instance.save()
            saved_products.append(instance.id)
            request.session["saved_products"] = saved_products
        serializer = self.get_serializer(instance)
        product_data = serializer.data
        return Response(product_data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def get_similar_products(self, request, pk=None):
        product = self.get_object()
        queryset = Product.objects.filter(category=product.category).exclude(
            id=product.id
        )[:6]
        serializer = ProductSerializer(queryset, many=True)
        pagination = self.paginate_queryset(queryset)
        if pagination is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def get_you_may_like(self, request, pk=None):
        product = self.get_object()
        queryset = (
            Product.objects.filter(category__category=product.category.category)
            .exclude(id=product.id)
            .order_by("-created_at")[:6]
        )
        serializer = ProductSerializer(queryset, many=True)
        pagination = self.paginate_queryset(queryset)
        if pagination is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def get_comments(self, request, pk=None):
        product = self.get_object()
        queryset = product.productcomment_set.all()
        serializer = ProductCommentSerializer(queryset, many=True, context={"request": request})
        pagination = self.paginate_queryset(queryset)
        if pagination is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def add_comment(self, request, pk=None):
        serializer = ProductCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, product_id=pk)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def like_comment(self, request, pk=None):
        serializer = CommentLikeSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["post"])
    def dislike_comment(self, request, pk=None):
        serializer = CommentDislikeSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def ask_question(self, request, pk=None):
        serializer = QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, product_id=pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def get_questions(self, request, pk=None):
        product = self.get_object()
        q_id = request.query_params.get("q_id", None)
        if q_id is not None:
            queryset = product.question_set.filter(id=q_id).last()
            serializer = QuestionSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            queryset = product.question_set.all()
        serializer = QuestionSerializer(queryset, many=True)
        pagination = self.paginate_queryset(queryset)
        if pagination is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def answer_question(self, request, pk=None):
        serializer = AnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class CartItemViewSet(viewsets.ViewSet):
    def list(self, request):
        if request.user.is_authenticated:
            queryset = CartItem.objects.filter(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            queryset = CartItem.objects.filter(session_key=request.session.session_key)
        serializer = CartItemSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def create(self, request):
        serializer = CartItemSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["delete"])
    def delete(self, request, pk=None):
        if request.user.is_authenticated:
            queryset = CartItem.objects.filter(user=request.user, id=pk)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            queryset = CartItem.objects.filter(
                session_key=request.session.session_key, id=pk
            )
        queryset.delete()
        return Response(status=204)

    @action(detail=True, methods=["post"])
    def add_one(self, request, pk=None):
        if request.user.is_authenticated:
            queryset = CartItem.objects.filter(user=request.user, id=pk)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            queryset = CartItem.objects.filter(
                session_key=request.session.session_key, id=pk
            )
        queryset.update(quantity=F("quantity") + 1)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def remove_one(self, request, pk=None):
        if request.user.is_authenticated:
            queryset = CartItem.objects.filter(user=request.user, id=pk)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            queryset = CartItem.objects.filter(
                session_key=request.session.session_key, id=pk
            )
        if queryset[0].quantity == 1:
            queryset.delete()
        else:
            queryset.update(quantity=F("quantity") - 1)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"])
    def clear(self, request):
        if request.user.is_authenticated:
            queryset = CartItem.objects.filter(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            queryset = CartItem.objects.filter(session_key=request.session.session_key)
        queryset.delete()
        return Response(status=204)

    @action(detail=False, methods=["get"])
    def get_card_info(self, request):
        if request.user.is_authenticated:
            queryset = CartItem.objects.filter(user=request.user).select_related('product')
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            queryset = CartItem.objects.filter(session_key=session_key).select_related('product')

        total_price = sum([item.product.price_with_discount * item.quantity for item in queryset])
        total_quantity = queryset.count()
        total_weight = queryset.aggregate(total_weight=Sum(F('product__weight') * F('quantity')))['total_weight']

        return Response(
            {
                "total_price": total_price,
                "total_quantity": total_quantity,
                "total_weight": total_weight,
            },
            status=status.HTTP_200_OK,
        )


class ProductLikeViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = ProductLikeSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def list(self, request):
        if request.user.is_authenticated:
            queryset = ProductLike.objects.filter(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            queryset = ProductLike.objects.filter(
                session_key=request.session.session_key
            )
        serializer = ProductLikeSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=True, methods=["delete"])
    def delete(self, request, pk=None):
        if request.user.is_authenticated:
            queryset = ProductLike.objects.filter(user=request.user, id=pk)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            queryset = ProductLike.objects.filter(
                session_key=request.session.session_key, id=pk
            )
        queryset.delete()
        return Response(status=204)

    @action(detail=False, methods=["delete"])
    def clear(self, request):
        if request.user.is_authenticated:
            queryset = ProductLike.objects.filter(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            queryset = ProductLike.objects.filter(
                session_key=request.session.session_key
            )
        queryset.delete()
        return Response(status=204)


class NewsletterViewSets(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    http_method_names = ["post"]
