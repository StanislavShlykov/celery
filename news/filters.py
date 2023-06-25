from django_filters import FilterSet, ModelChoiceFilter, DateFromToRangeFilter, RangeFilter
from django_filters.widgets import RangeWidget
from .models import Post, Category


class PostFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Category')

    date = DateFromToRangeFilter(
        field_name='time_in',
        widget=RangeWidget(attrs={'placeholder': 'MM/DD/YYYY'}),
        label='Date')


    class Meta:
        model = Post
        fields = {
            'post_name': ['icontains'],
            'author': ['exact'],
    }
