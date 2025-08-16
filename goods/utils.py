from django.db.models import Q
import re
from goods.models import Products

def q_search(query):
    if query.isdigit() and len(query) <= 5:
        return Products.objects.filter(id=int(query))

    results = Products.objects.filter(
        Q(name__icontains=query) | 
        Q(description__icontains=query)
    ).distinct()

    # Создаем регулярное выражение для поиска без учета регистра
    pattern = re.compile(f'({re.escape(query)})', re.IGNORECASE)

    for product in results:
        # Подсветка в названии
        product.headline = pattern.sub(
            r'<span style="background-color: yellow;">\1</span>',
            product.name
        )
        
        # Подсветка в описании
        if product.description:
            product.bodyline = pattern.sub(
                r'<span style="background-color: yellow;">\1</span>',
                product.description
            )
        else:
            product.bodyline = ""

    return results