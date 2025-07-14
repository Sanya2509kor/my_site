from django.http import Http404
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
    
    
# def catalog(request, category_slug=None):

#     page = request.GET.get('page', 1)
#     on_sale = request.GET.get('on_sale', None)
#     order_by = request.GET.get('order_by', None)
#     query = request.GET.get('q', None)

#     if category_slug == 'all':
#         goods = Products.objects.all()
#     elif query:
#         goods = q_search(query)
#     else:
#         goods = Products.objects.filter(category__slug=category_slug)
#         if not goods.exists():
#             raise Http404()
    

#     if on_sale:
#         goods = goods.filter(discount__gt=0)

#     if order_by and order_by != "default":
#         goods = goods.order_by(order_by)

#     goods = goods.filter(quantity__gt=0)

#     paginator = Paginator(goods, 21)
#     current_page = paginator.page(int(page))

#     context = {
#         'title': 'Home - Каталог',
#         'goods': current_page,
#         'slug_url': category_slug,
#     }
#     return render(request, 'goods/catalog.html', context)



class ProductView(DetailView):

    template_name = 'goods/product.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    queryset = Products.objects.prefetch_related('related_products')  # Оптимизация


    def get_object(self, queryset=None):
        product = Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        context['related_products'] = self.object.related_products.all()[:6]  # Ограничиваем до 6 товаров
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