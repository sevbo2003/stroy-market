from rest_framework import serializers
from apps.stroy.models import Category, SubCategory, Product, ProductImage, Size, Color


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name_uz', 'name_ru', 'slug', 'image')


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'name_uz', 'name_ru', 'slug', 'image', 'category')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'product', 'image')


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('id', 'name_uz', 'name_ru', 'product')


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('id', 'name_uz', 'name_ru', 'product')


class ProductSerializer(serializers.ModelSerializer):
    category = SubCategorySerializer()
    images = serializers.SerializerMethodField()
    sizes = serializers.SerializerMethodField()
    colors = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'price_with_discount', 'in_discount', 'discount_percent', 'category', 'count', 'weight', 'product_type', 'images', 'sizes', 'colors', 'control', 'purpose', 'material', 'xususiyatlari', 'brand', 'sotuvchi', 'description', 'views', 'like_count', 'created_at']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['likes'] = None
        return data

    def get_images(self, obj):
        queryset = obj.productimage_set.all()
        serializer = ProductImageSerializer(queryset, many=True)
        return serializer.data

    def get_sizes(self, obj):
        queryset = obj.size_set.all()
        serializer = SizeSerializer(queryset, many=True)
        return serializer.data
    
    def get_colors(self, obj):
        queryset = obj.color_set.all()
        serializer = ColorSerializer(queryset, many=True)
        return serializer.data
    