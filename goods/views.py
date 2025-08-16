from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from goods.models import Products
from goods.utils import q_search



class CatalogView(ListView):
    model = Products
    # queryset = Products.objects.all().order_by("-id")
    template_name = 'goods/catalog.html'
    context_object_name = 'goods'
    paginate_by = 15
    allow_empty = True


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        context['slug_url'] = self.kwargs.get("category_slug") 

        # if 'goods' in context:
        #     for product in context['goods']:
        #         product.related_products_list = product.related_products.all()[:4]  # Ограничиваем до 4 товаров
        return context
    
    def get_queryset(self):
        
        category_slug = self.kwargs.get("category_slug")
        on_sale = self.request.GET.get("on_sale")
        order_by = self.request.GET.get("order_by")
        query = self.request.GET.get("q")

        if category_slug == 'all':
            goods = Products.objects.all()
        elif query:
            goods = q_search(query)
        else:
            goods = Products.objects.filter(category__slug=category_slug)
            # if not goods.exists():
            #     raise Http404()
        

        if on_sale:
            goods = goods.filter(discount__gt=0)

        if order_by and order_by != "default":
            goods = goods.order_by(order_by)

        goods = goods.filter(quantity__gt=0)

        return goods.prefetch_related('related_products')  # Оптимизация запросов
    

class ProductView(DetailView):

    template_name = 'goods/product.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    queryset = Products.objects.prefetch_related('related_products')  # Оптимизация


    def get_object(self, queryset=None):
        product_slug = self.kwargs.get(self.slug_url_kwarg)
        color = self.request.GET.get('color')
        size = self.request.GET.get('size')
        power = self.request.GET.get('power')

        # Получаем базовый продукт
        base_product = get_object_or_404(Products, slug=product_slug)
        
        # Если есть параметры цвета или размера, ищем конкретную вариацию
        if color or size or power:
            filters = {
                'name': base_product.name,
            }
            if color:
                filters['color'] = color
            if size:
                filters['size'] = size
            if power:
                filters['power'] = power
            
            try:
                product = Products.objects.filter(**filters).first()
                return product
            except Products.DoesNotExist:
                # Если конкретная вариация не найдена, возвращаем базовый продукт
                return base_product
        return base_product
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        # Текущие параметры
        current_color = self.request.GET.get('color', product.color)
        current_size = self.request.GET.get('size', product.size)
        current_power = self.request.GET.get('power', product.power)
        
        # Базовый запрос
        base_query = Products.objects.filter(name=product.name)
        
        # Доступные мощности (учитываем выбранные цвет и размер)
        available_powers_query = base_query
        if current_color:
            available_powers_query = available_powers_query.filter(color=current_color)
        if current_size:
            available_powers_query = available_powers_query.filter(size=current_size)
        
        available_powers = available_powers_query.exclude(
            power__isnull=True
        ).values_list('power', flat=True).distinct()
        
        # Доступные размеры (учитываем выбранные цвет и мощность)
        available_sizes_query = base_query
        if current_color:
            available_sizes_query = available_sizes_query.filter(color=current_color)
        if current_power:
            available_sizes_query = available_sizes_query.filter(power=current_power)
        
        available_sizes = available_sizes_query.exclude(
            size__isnull=True
        ).values_list('size', flat=True).distinct()
        
        # Доступные цвета (учитываем выбранные размер и мощность)
        available_colors_query = base_query
        if current_size:
            available_colors_query = available_colors_query.filter(size=current_size)
        if current_power:
            available_colors_query = available_colors_query.filter(power=current_power)
        
        available_colors = available_colors_query.exclude(
            color__isnull=True
        ).values_list('color', flat=True).distinct()
        
        # Формируем список цветов с информацией о доступности
        color_choices = []
        all_colors = base_query.exclude(color__isnull=True).values_list('color', flat=True).distinct()
        
        for color_value, color_name in Products.COLOR:
            if color_value in all_colors:
                is_available = color_value in available_colors
                color_choices.append({
                    'value': color_value,
                    'name': color_name,
                    'available': is_available,
                    'current': color_value == current_color
                })


        context['title'] = self.object.name
        context['related_products'] = self.object.related_products.all()
        context['colors'] = color_choices if len(available_sizes) > 0 else False
        context['sizes'] = available_sizes if len(available_sizes) > 1 else False
        context['available_powers'] = available_powers if len(available_powers) > 1 else False
        context['current_color'] = current_color
        context['current_size'] = current_size
        context['current_power'] = current_power
        context['base_product_slug'] = product.slug
        return context



# def product(request, product_slug):
#     product = Products.objects.get(slug=product_slug)

#     context = {
#         "product": product, 
#     }
#     return render(request, 'goods/product.html', context=context)



class SubCatalogView(ListView):
    model = Products
    # queryset = Products.objects.all().order_by("-id")
    template_name = 'goods/catalog.html'
    context_object_name = 'goods'
    paginate_by = 15
    allow_empty = True



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        context['slug_url'] = self.kwargs.get("subcategory_slug") 

        # if 'goods' in context:
        #     for product in context['goods']:
        #         product.related_products_list = product.related_products.all()[:4]  # Ограничиваем до 4 товаров
        return context
    
    def get_queryset(self):
        
        subcategory_slug = self.kwargs.get("subcategory_slug")
        on_sale = self.request.GET.get("on_sale")
        order_by = self.request.GET.get("order_by")
        query = self.request.GET.get("q")

        if subcategory_slug == 'all':
            goods = Products.objects.all()
        elif query:
            goods = q_search(query)
        else:
            goods = Products.objects.filter(subcategory__slug=subcategory_slug)
            # if not goods.exists():
            #     raise Http404()
        

        if on_sale:
            goods = goods.filter(discount__gt=0)

        if order_by and order_by != "default":
            goods = goods.order_by(order_by)

        goods = goods.filter(quantity__gt=0)

        return goods.prefetch_related('related_products')  # Оптимизация запросов