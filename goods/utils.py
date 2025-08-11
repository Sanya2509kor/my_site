from re import search
from django.db.models import Q
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    SearchHeadline,
)

from goods.models import Products


def q_search(query):
    if query.isdigit() and len(query) <= 5:
        return Products.objects.filter(id=int(query))

    vector = SearchVector("name", "description")
    query = SearchQuery(query)

    result = (
        Products.objects.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0)
        .order_by("-rank")
    )
    result = result.annotate(
        headline=SearchHeadline(
            "name", 
            query, 
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        )
    )
    result = result.annotate(
        bodyline=SearchHeadline(
            "description",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        )
    )

    return result
    




# для деплоя


# from django.db.models import Q
# import re
# from goods.models import Products

# def q_search(query):
#     if query.isdigit() and len(query) <= 5:
#         return Products.objects.filter(id=int(query))

#     results = Products.objects.filter(
#         Q(name__icontains=query) | 
#         Q(description__icontains=query)
#     ).distinct()

#     # Создаем регулярное выражение для поиска без учета регистра
#     pattern = re.compile(f'({re.escape(query)})', re.IGNORECASE)

#     for product in results:
#         # Подсветка в названии
#         product.headline = pattern.sub(
#             r'<span style="background-color: yellow;">\1</span>',
#             product.name
#         )
        
#         # Подсветка в описании
#         if product.description:
#             product.bodyline = pattern.sub(
#                 r'<span style="background-color: yellow;">\1</span>',
#                 product.description
#             )
#         else:
#             product.bodyline = ""

#     return results