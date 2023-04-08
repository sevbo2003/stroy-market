from django.db import models
from apps.stroy.models import Product

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
        return f'{self.recommendation.title} - {self.product.title}'
    
    class Meta:
        verbose_name = 'Recommendation Product'
        verbose_name_plural = 'Recommendation Products'
        ordering = ['-created_at']
