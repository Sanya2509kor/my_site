from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from goods.models import Categories, Products
from goods.utils import q_search



class IndexView(ListView):
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
        return context
    
    def get_queryset(self):
        
        category_slug = self.kwargs.get("category_slug")
        on_sale = self.request.GET.get("on_sale")
        order_by = self.request.GET.get("order_by")
        query = self.request.GET.get("q")

        if category_slug == 'all' or category_slug == None:
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


class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - о нас'
        context['content'] = 'Страница о нас'
        context['text_on_page'] = 'Тут будет написана вся информация о нашей компании!' 
        return context


# def about(request):
#     contex = {
#         'title': 'Home - О нас',
#         'content': 'Страница О нас',
#         'text_on_page': "Тут будет написана вся информация о нашей компании!"
#     }

#     return render(request, 'main/about.html', contex)


class ContactsView(TemplateView):
    template_name = 'main/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        context['content'] = 'Наши контакты'
        context['text_on_page'] = 'Контакты, адрес, и другая информация'
        return context



class DeliveryView(TemplateView):
    template_name = 'main/delivery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Доставка и оплата'
        context['content'] = 'Доставка и Оплата'
        context['text_on_page'] = 'Описание как происходит доставка, и т.д'
        return context