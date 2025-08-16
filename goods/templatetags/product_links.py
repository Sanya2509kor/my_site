from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
import re

from goods.models import Products

register = template.Library()

@register.filter
def make_product_links(text):
    # Находим все совпадения вида GARDINA2 01, SHTORKA 01 и т.д.
    pattern = r'\b([A-Z]+[0-9]* [0-9]{2})\b'
    
    def replace_match(match):
        product_code = match.group(1)
        try:
            # Ищем товар по коду (предполагая, что код хранится в поле name)
            product = Products.objects.get(name__contains=product_code)
            url = reverse('catalog:product', kwargs={'product_slug': product.slug})
            return f'<a href="{url}" class="product-link">{product_code}</a>'
        except Products.DoesNotExist:
            return product_code
    
    return mark_safe(re.sub(pattern, replace_match, text))