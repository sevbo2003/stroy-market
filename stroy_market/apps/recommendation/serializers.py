from rest_framework import serializers
from .models import (
    Recommendation,
    RecommendationProduct,
    RecommentationForCart,
    RecommendationForCartProduct,
)
from apps.stroy.serializers import ProductSerializer


class RecommendationProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = RecommendationProduct
        fields = ('product',)

    
class RecommendationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recommendation
        fields = ('id', 'title_uz', 'title_ru')


class RecommentationForCartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = RecommendationForCartProduct
        fields = ('product',)


class RecommentationForCartSerailizer(serializers.ModelSerializer):
        products = serializers.SerializerMethodField()

        class Meta:
            model = RecommentationForCart
            fields = ('id', 'title_uz', 'title_ru', 'products')
        
        def get_products(self, obj):
            queryset = RecommendationForCartProduct.objects.filter(recommendation_id=obj.id)
            serializer = RecommentationForCartProductSerializer(queryset, many=True)
            return serializer.data
