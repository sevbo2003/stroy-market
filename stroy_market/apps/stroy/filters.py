from django_filters import rest_framework as filters
from apps.stroy.models import Category, SubCategory, Product, ProductImage, Size, Color


class ProductFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category__category__slug')
    subcategory = filters.CharFilter(field_name='subcategory__slug')
    view = filters.BooleanFilter(method='popular')
    count = filters.BooleanFilter(method='latest')

    class Meta:
        model = Product
        fields = ['category', 'subcategory', 'view', 'count']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['category'].label = 'Kategoriya'
        self.filters['subcategory'].label = 'Sub kategoriya'
        self.filters['view'].label = 'Mashhur'
        self.filters['count'].label = 'Recommended'
    
    def popular(self, queryset, name, value):
        if value:
            return queryset.order_by('-views')
        elif value == False:
            return queryset.order_by('views')
        return queryset

    def latest(self, queryset, name, value):
        if value:
            return queryset.order_by('-created_at')
        return queryset.order_by('created_at')
