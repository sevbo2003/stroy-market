from rest_framework import serializers
from .models import Recommendation, RecommendationProduct
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
