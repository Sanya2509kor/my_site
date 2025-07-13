from django import template
from django.utils.http import urlencode

from goods.models import Categories, SubCategories


register = template.Library()

@register.simple_tag()
def tag_categories():
    categories = Categories.objects.all().prefetch_related('subcategories_set')
    return categories

    # return Categories.objects.all()


@register.simple_tag()
def tag_subcategories():
    subcategories = SubCategories.objects.all()    
    return subcategories


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)