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


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name_uz', 'name_ru', 'price', 'count', 'weight', 'category', 'subcategory', 'product_type_uz', 'product_type_ru', 'control_uz', 'control_ru', 'purpose_uz', 'purpose_ru', 'material_uz', 'material_ru', 'xususiyatlari_uz', 'xususiyatlari_ru', 'brand_uz', 'brand_ru', 'sotuvchi_uz', 'sotuvchi_ru', 'description_uz', 'description_ru')


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

