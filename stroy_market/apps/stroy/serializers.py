from rest_framework import serializers
from apps.stroy.models import Category, SubCategory, Product, ProductImage, Size, Color, ProductComment, CommentLike, CartItem, ProductLike, Newsletter, Question, Answer
from django.conf import settings
from .validators import validate_star_rating

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name_uz', 'name_ru', 'slug', 'image')


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'name_uz', 'name_ru', 'slug', 'image', 'category', 'banner', 'width', 'height', 'banner_link')

    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data['image'] = settings.BASE_URL + data['image']
        return data


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
    
    def validate_stars(self, value):
        validate_star_rating(value)
        return value
    
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
        comment_like = CommentLike.objects.filter(comment=comment, user=user).last()
        if comment_like:
            if like:
                comment_like.like = True
                comment_like.dislike = False
            else:
                comment_like.like = False
                comment_like.dislike = True
            comment_like.save()
            return comment_like
        return super().create(validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    quantity = serializers.IntegerField(required=False, default=1)

    class Meta:
        model = CartItem
        fields = ['id', 'product','session_key', 'quantity', 'user', 'date_added']
        read_only_fields = ('user', 'session_key', 'date_added')

    def create(self, validated_data):
        request = self.context.get('request')
        if request.user.is_authenticated:
            validated_data['user'] = request.user
            cart_item = CartItem.objects.filter(user=request.user, product=validated_data['product']).last()
            if cart_item:
                cart_item.quantity += validated_data['quantity']
                cart_item.save()
                return cart_item
            return super().create(validated_data)
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        validated_data['session_key'] = session_key
        cart_item = CartItem.objects.filter(session_key=session_key, product=validated_data['product']).last()
        if cart_item:
            cart_item.quantity += validated_data['quantity']
            cart_item.save()
            return cart_item
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
        read_only_fields = ("user", "session_key")
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request.user.is_authenticated:
            if ProductLike.objects.filter(user=request.user, product=validated_data['product']).exists():
                raise serializers.ValidationError('You have already liked this product')
            validated_data['user'] = request.user
            return super().create(validated_data)
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        if ProductLike.objects.filter(session_key=session_key, product=validated_data['product']).exists():
            raise serializers.ValidationError('You have already liked this product')
        validated_data['session_key'] = session_key
        return super().create(validated_data)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['product'] = ProductSerializer(instance.product).data
        data['image'] = settings.BASE_URL + instance.product.productimage_set.first().image.url
        data['session_key'] = None
        return data


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ('id', 'phone_number', 'created_at')
        read_only_fields = ('created_at',)


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField(required=False, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'user', 'product', 'question','answers', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'user', 'product')

    def get_answers(self, obj):
        answers = Answer.objects.filter(question=obj)
        return AnswerSerializer(answers, many=True).data
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = instance.user.full_name
        return data
    

class AnswerSerializer(serializers.ModelSerializer):
    by_admin = serializers.BooleanField(read_only=True)

    class Meta:
        model = Answer
        fields = ('id', 'question', 'answer', 'by_admin', 'created_at', 'updated_at')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['question'] = instance.question.question
        return data
    