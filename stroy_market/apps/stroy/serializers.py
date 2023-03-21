from rest_framework import serializers
from apps.stroy.models import Category, SubCategory, Product, ProductImage, Size, Color, ProductComment, CommentLike, CartItem, ProductLike, BestProduct, PopularProduct, Newsletter, RecommendedProduct, Question, Answer
from django.conf import settings
from django.contrib.sessions.models import Session


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
        data['user'] = instance.user.full_name
        data['likes'] = instance.commentlike_set.filter(like=True).count()
        data['dislikes'] = instance.commentlike_set.filter(dislike=True).count()
        return data
    

class CommentLikeSerializer(serializers.ModelSerializer):
    like = serializers.BooleanField(required=False)
    dislike = serializers.BooleanField(required=False)

    class Meta:
        model = CommentLike
        fields = ('id', 'comment', 'user', 'like', 'dislike')
        read_only_fields = ('user', 'created_at')

    def create(self, validated_data):
        like = validated_data.get('like', None)
        dislike = validated_data.get('dislike', None)
        if like and dislike:
            raise serializers.ValidationError('Like and dislike can not be true at the same time')
        if not like and not dislike:
            raise serializers.ValidationError('Like or dislike must be true')
        comment = validated_data.get('comment')
        user = validated_data.get('user')
        if CommentLike.objects.filter(comment=comment, user=user).exists():
            raise serializers.ValidationError('You have already liked or disliked this comment')
        return super().create(validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    user = serializers.StringRelatedField()
    quantity = serializers.IntegerField(required=False, default=1)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'user', 'date_added']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
            return super().create(validated_data)
        
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key

        validated_data['session_key'] = session_key
        return super().create(validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['product'] = ProductSerializer(instance.product).data
        data['price'] = instance.product.price_with_discount * instance.quantity
        data['image'] = settings.BASE_URL + instance.product.productimage_set.first().image.url
        return data


class ProductLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLike
        fields = ("id", "user", "session_key", "product")
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
            return super().create(validated_data)
        
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key

        validated_data['session_key'] = session_key
        return super().create(validated_data)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['product'] = ProductSerializer(instance.product).data
        data['image'] = settings.BASE_URL + instance.product.productimage_set.first().image.url
        return data


class BestProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = BestProduct
        fields = ('id', 'product', 'created_at')


class PopularProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = PopularProduct
        fields = ('id', 'product', 'created_at')


class RecommendedProductSerializer(serializers.Serializer):
    product = ProductSerializer()

    class Meta:
        model = RecommendedProduct
        fields = ('id', 'product', 'created_at')

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ('id', 'phone_number', 'created_at')
        read_only_fields = ('created_at',)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'user', 'product', 'question', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'user', 'product')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = instance.user.full_name
        return data
    

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'question', 'answer', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'question')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['question'] = instance.question.question
        return data
    
    def create(self, validated_data):
        user = self.context.get('request').user
        if user.is_superuser:
            return super().create(validated_data)
        raise serializers.ValidationError('You are not allowed to answer questions')
    