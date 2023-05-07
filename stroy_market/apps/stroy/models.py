from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.sessions.models import Session
from apps.authentication.validators import validate_uzb_phone_number
from apps.stroy.tasks import send_news

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=125, verbose_name=_('Category name'))
    image = models.ImageField(upload_to='category')
    slug = models.SlugField(max_length=125, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('name',)


class SubCategory(models.Model):
    name = models.CharField(max_length=125, verbose_name=_('SubCategory name'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='category')
    slug = models.SlugField(max_length=125, unique=True, blank=True, null=True)
    banner = models.ImageField(upload_to='category-banners', blank=True, null=True)
    banner_link = models.URLField(blank=True, null=True)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('SubCategory')
        verbose_name_plural = _('SubCategories')
        ordering = ('name',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)


class Product(models.Model):
    TYPE = (
        ('dona', 'шт'),
        ('m2', 'м2'),
    )
    name = models.CharField(max_length=125)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_discount = models.BooleanField(default=False, null=True, blank=True)
    discount_percent = models.PositiveIntegerField(null=True, blank=True)
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    rating = models.FloatField(default=0)
    comments = models.IntegerField(default=0)
    product_type = models.CharField(max_length=125, choices=TYPE, default='m2', null=True, blank=True)
    control = models.CharField(max_length=125, null=True, blank=True)
    purpose = models.CharField(max_length=125, null=True, blank=True)
    material = models.CharField(max_length=125, null=True, blank=True)
    xususiyatlari = models.CharField(max_length=125, null=True, blank=True)
    brand = models.CharField(max_length=125, null=True, blank=True)
    sotuvchi = models.CharField(max_length=125, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    @property
    def price_with_discount(self):
        if self.in_discount:
            return self.price - self.price * self.discount_percent / 100
        return self.price

    @property
    def avarage_rating(self):
        if self.rating == 0:
            return 0
        if self.comments == 0:
            return 0
        else:
            return self.rating / self.comments

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product')

    def __str__(self):
        return self.product.name


class Size(models.Model):
    name = models.CharField(max_length=125)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class Color(models.Model):
    name = models.CharField(max_length=125)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# write star validator with 0.5 step


class ProductComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    stars = models.FloatField()
    comment = models.TextField()
    likes = models.ManyToManyField(User, related_name='likes', blank=True, null=True)
    dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + ' ' + self.product.name + ' ' + str(self.stars)
    
    def save(self, *args, **kwargs):
        product = self.product
        product.rating += self.stars
        product.comments += 1
        product.save()
        super(ProductComment, self).save(*args, **kwargs)
    
    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def dislikes_count(self):
        return self.dislikes.count()

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('ProductComment')
        verbose_name_plural = _('Product Comments') 


class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey('ProductComment', on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + ' ' + self.comment.product.name + ' ' + str(self.like) + ' ' + str(self.dislike)

    class Meta:
        verbose_name = _('Comment Like')
        verbose_name_plural = _('Comment Likes')


class CartItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    def total_price(self):
        return self.product.price * self.quantity


class ProductLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = _('Saqlangan mahsulot')
        verbose_name_plural = _('Saqlangan mahsulotlar')
    

class PromoCode(models.Model):
    code = models.CharField(max_length=125)
    discount = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _('Promo code')
        verbose_name_plural = _('Promo codes')



class Newsletter(models.Model):
    phone_number = models.CharField(max_length=20, validators=[validate_uzb_phone_number])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = _('Foydalanuvchi')
        verbose_name_plural = _('Foydalanuvchilar')


class News(models.Model):
    message = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    
    class Meta:
        verbose_name = _('Xabarnoma')
        verbose_name_plural = _('Xabarnomalar')
        ordering = ('-created_at',)
    
    def save(self, *args, **kwargs):
        super(News, self).save(*args, **kwargs)
        message = self.message
        numbers = list(Newsletter.objects.all().values_list('phone_number', flat=True))
        send_news.apply_async(args=[numbers, message])


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.full_name + ' ' + self.product.name
    
    class Meta:
        verbose_name = _('Savol')
        verbose_name_plural = _('Savollar')
        ordering = ('-created_at',)
    

class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    by_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question.user.full_name + ' ' + self.question.product.name
    
    class Meta:
        verbose_name = _('Javob')
        verbose_name_plural = _('Javoblar')
        ordering = ('-created_at',)
        