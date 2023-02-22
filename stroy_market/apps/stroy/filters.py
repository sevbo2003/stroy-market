from django_filters import rest_framework as filters
from apps.stroy.models import Category, SubCategory, Product, ProductImage, Size, Color


class ProductFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category__category__slug')
    subcategory = filters.CharFilter(field_name='subcategory__slug')
    popular = filters.BooleanFilter(method_name='popular')
    latest = filters.BooleanFilter(method_name='latest')

    class Meta:
        model = Product
        fields = ['category', 'subcategory', 'popular', 'latest']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['category'].label = 'Kategoriya'
        self.filters['subcategory'].label = 'Sub kategoriya'
        self.filters['popular'].label = 'Mashhur'
        self.filters['latest'].label = 'Yangi'
    
    def popular(self, queryset, name, value):
        if value:
            return queryset.order_by('-count')
        return queryset.order_by('count')

    def latest(self, queryset, name, value):
        if value:
            return queryset.order_by('-created_at')
        return queryset.order_by('created_at')
