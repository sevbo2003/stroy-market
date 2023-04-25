from rest_framework import serializers
from .models import (
    Recommendation,
    RecommendationProduct,
    RecommentationForCart,
    RecommendationForCartProduct,
    RecommendationForProductDetail,
    RecommendationForProductDetailProduct,
    SpecialOffer,
    RecommendationForCategory,
    RecommendationForCategoryProduct,
)
from apps.stroy.serializers import ProductSerializer
from django.conf import settings


class RecommendationProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = RecommendationProduct
        fields = ("product",)


class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = ("id", "title_uz", "title_ru")


class RecommentationForCartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = RecommendationForCartProduct
        fields = ("product",)


class RecommentationForCartSerailizer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = RecommentationForCart
        fields = ("id", "title_uz", "title_ru", "products")

    def get_products(self, obj):
        queryset = RecommendationForCartProduct.objects.filter(recommendation_id=obj.id)
        serializer = RecommentationForCartProductSerializer(queryset, many=True)
        return serializer.data


class RecommendationForProductDetailProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = RecommendationForProductDetailProduct
        fields = ("product",)


class RecommendationForProductDetailSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = RecommendationForProductDetail
        fields = ("id", "title_uz", "title_ru", "products")

    def get_products(self, obj):
        queryset = RecommendationForProductDetailProduct.objects.filter(
            recommendation_id=obj.id
        )
        serializer = RecommendationForProductDetailProductSerializer(
            queryset, many=True
        )
        return serializer.data


class SpecialOfferSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = SpecialOffer
        fields = ("id", "category", "product", "image", "created_at", "updated_at")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["image"] = settings.BASE_URL + data["image"]
        return data


class RecommendationForCategoryProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = RecommendationForCategoryProduct
        fields = ("product",)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data


class RecommendationForCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationForCategory
        fields = ("id", "title_uz", "title_ru", "category", "created_at", "updated_at")
