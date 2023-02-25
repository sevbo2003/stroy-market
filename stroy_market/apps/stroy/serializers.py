from rest_framework import serializers
from apps.stroy.models import Category, SubCategory, Product, ProductImage, Size, Color, ProductComment
from django.conf import settings


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name_uz', 'name_ru', 'slug', 'image')


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'name_uz', 'name_ru', 'slug', 'image', 'category')


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ('id', 'product', 'image')
    
    def get_image(self, obj):
        return settings.BASE_URL + obj.image.url


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
        fields = ['id', 'name_uz', 'name_ru', 'price', 'price_with_discount', 'in_discount', 'discount_percent', 'category', 'count', 'weight', 'product_type', 'images', 'sizes', 'colors', 'control', 'purpose', 'material', 'xususiyatlari', 'brand', 'sotuvchi', 'description', 'views', 'avarage_rating', 'comments', 'created_at']
    
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


class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = ('id', 'product', 'user', 'comment', 'stars', 'created_at')
        read_only_fields = ('user', 'created_at')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = instance.user.first_name + ' ' + instance.user.last_name
        return data
    