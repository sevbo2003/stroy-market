from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.sessions.models import Session


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
    

class ProductComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment = models.TextField()
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
        return self.product

    class Meta:
        verbose_name = _('Saqlangan mahsulot')
        verbose_name_plural = _('Saqlangan mahsulotlar')
        