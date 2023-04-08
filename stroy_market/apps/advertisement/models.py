from django.db import models
from apps.stroy.models import SubCategory


class Banner(models.Model):
    image = models.ImageField(upload_to='banners/')
    is_active = models.BooleanField(default=True)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    banner_link = models.URLField(blank=True, null=True)


    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"
        