from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from goods.models import Categories



class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Главная'
        context['content'] = 'СеАл'
        return context

# def index(request):

#     contex = {
#         'title': 'Home - Главная',
#         'content': 'Магазин мебели HOME',
#     }

#     return render(request, 'main/index.html', contex)


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