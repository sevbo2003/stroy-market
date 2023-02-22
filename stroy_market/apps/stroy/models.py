from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=125, verbose_name=_('Category name'))
    image = models.ImageField(upload_to='category')
    slug = models.SlugField(max_length=125, unique=True)

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
