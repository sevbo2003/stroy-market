from django.db import models
from apps.stroy.models import SubCategory


class Banner(models.Model):
    image = models.ImageField(upload_to='banners/')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.sub_category.name

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"
        