from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth import get_user_model

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
    in_discount = models.BooleanField(default=False)
    discount_percent = models.PositiveIntegerField(null=True, blank=True)
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    count = models.IntegerField()
    weight = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    product_type = models.CharField(max_length=125, choices=TYPE, default='m2')
    control = models.CharField(max_length=125)
    purpose = models.CharField(max_length=125)
    material = models.CharField(max_length=125)
    xususiyatlari = models.CharField(max_length=125)
    brand = models.CharField(max_length=125)
    sotuvchi = models.CharField(max_length=125)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField()

    @property
    def like_count(self):
        return self.likes.count()
    
    @property
    def price_with_discount(self):
        if self.in_discount:
            return self.price - self.price * float(self.discount_percent)
        return self.price


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
    