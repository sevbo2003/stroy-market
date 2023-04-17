from django.db import models
from apps.stroy.models import Product, Category

class Recommendation(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Recommendation'
        verbose_name_plural = 'Recommendations'
        ordering = ['-updated_at']


class RecommendationProduct(models.Model):
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.recommendation.title} - {self.product.name}'
    
    class Meta:
        verbose_name = 'Recommendation Product'
        verbose_name_plural = 'Recommendation Products'
        ordering = ['-created_at']



class RecommentationForCart(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Savatcha uchun tavsiya'
        verbose_name_plural = 'Savatcha uchun tavsiyalar'
        ordering = ['-created_at']


class RecommendationForCartProduct(models.Model):
    recommendation = models.ForeignKey(RecommentationForCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.recommendation.title} - {self.product.name}'
    
    class Meta:
        verbose_name = 'Savatcha uchun tavsiya mahsulot'
        verbose_name_plural = 'Savatcha uchun tavsiya mahsulot'
        ordering = ['-created_at']


class RecommendationForProductDetail(models.Model):
    title = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Recommendation for product detail'
        verbose_name_plural = 'Recommendations for product detail'
        ordering = ['-created_at']


class RecommendationForProductDetailProduct(models.Model):
    recommendation = models.ForeignKey(RecommendationForProductDetail, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.recommendation.title} - {self.product.name}'
    
    class Meta:
        verbose_name = 'Recommendation Product detail product'
        verbose_name_plural = 'Recommendation Products detail product'
        ordering = ['-created_at']


class SpecialOffer(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='special-offer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Special offer'
        verbose_name_plural = 'Special offers'
        ordering = ['-created_at']

class RecommendationForCategory(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Recommendation for category'
        verbose_name_plural = 'Recommendations for categories'
        ordering = ['-updated_at']


class RecommendationForCategoryProduct(models.Model):
    recommendation = models.ForeignKey(RecommendationForCategory, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.recommendation.title} - {self.product.name}'
    
    class Meta:
        verbose_name = 'Recommendation for category product'
        verbose_name_plural = 'Recommendation for category products'
        ordering = ['-created_at']
