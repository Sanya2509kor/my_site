from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from goods.models import Categories



class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - главная'
        context['content'] = 'Магазин мебели HOME'
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
