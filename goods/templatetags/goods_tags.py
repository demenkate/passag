from django import template
from django.utils.http import urlencode
from django.db.models import Case, When, Value, IntegerField, Sum, Q


from goods.models import Categories, Products


register = template.Library()


@register.simple_tag()
def tag_categories():
    return Categories.objects.annotate(
        product_count=Sum('products__sizeproductrelation__count'),
        is_all=Case(
            When(slug='all', then=Value(0)),
            default=Value(1),
            output_field=IntegerField()
        )
    ).filter(Q(product_count__gt=0) | Q(slug='all')).order_by('is_all', 'id')


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    # example with other context vars
    # print(context['title'])
    # print(context['slug_url'])
    # print(context['goods'])
    # print([product.name for product in context['goods']])
    query.update(kwargs)
    return urlencode(query)


@register.simple_tag()
def products(slug):
    return Products.objects.filter(category__slug=slug)

