from .models import Movie, Member_data
import django_filters
from django import forms


class MovieFilter(django_filters.FilterSet):
    search_type = django_filters.ChoiceFilter(
        choices=[
            ('movie_name', '電影名稱'),
            ('date', '上映日期'),
            ('type', '類型')
        ],
        method='filter_by_type',
        widget=forms.Select(attrs={'class': 'form-control dropdown-toggle'})
    )
    search_text = django_filters.CharFilter(
        field_name='search_text',
        label='Search',
        method='filter_by_type',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Movie
        fields = []

    def filter_by_type(self, queryset, name, value):
        search_type = self.data.get('search_type')
        search_text = self.data.get('search_text')
        if search_type and search_text:
            filter_kwargs = {f"{search_type}__icontains": search_text}
            return queryset.filter(**filter_kwargs)
        return queryset


class MemberFilter(django_filters.FilterSet):
    gmail = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Member_data
        fields = '__all__'


class MovieTypeFilter(django_filters.FilterSet):
    search_type = django_filters.ChoiceFilter(
        choices=[
            ('movie_name', '電影名稱'),
            ('type', '電影類型')
        ],
        empty_label='請選擇',
        method='filter_by_type',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    search_text = django_filters.CharFilter(
        field_name='search_text',
        label='Search',
        method='filter_by_type',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Movie
        fields = []

    def filter_by_type(self, queryset, name, value):
        search_type = self.data.get('search_type')
        search_text = self.data.get('search_text')
        if search_type and search_text:
            filter_kwargs = {f"{search_type}__icontains": search_text}
            return queryset.filter(**filter_kwargs)
        return queryset
