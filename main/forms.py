from django import forms
from goods.models import Categories
from django.db.models import Q, Sum


class ExportForm(forms.Form):

    category = forms.ModelChoiceField(queryset=Categories.objects.annotate(product_count=Sum('products__sizeproductrelation__count')).filter(Q(product_count__gt=0)), required=True)
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}), required=False)