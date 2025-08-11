from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Count, Prefetch, Q
from examples.models import Examples, ListImages


class ExamplesView(ListView):
    template_name = 'examples/examples.html'
    context_object_name = 'examples'
    paginate_by = 15
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Примеры работ',
            'meta_description': 'Примеры наших работ и выполненных проектов',
            'active_tab': 'examples'
        })
        return context
    
    def get_queryset(self):
        # Правильная аннотация количества изображений
        queryset = Examples.objects.prefetch_related(
            Prefetch(
                'images',
                queryset=ListImages.objects.order_by('id'),
                to_attr='prefetched_images'
            )
        ).annotate(
            images_count=Count('images')
        ).order_by('-id')
        
        # Добавляем флаг наличия изображений через дополнительное поле
        for example in queryset:
            example.has_images = example.images_count > 0
            
        return queryset

    def get_paginate_by(self, queryset):
        if 'paginate_by' in self.request.GET:
            try:
                return int(self.request.GET.get('paginate_by'))
            except ValueError:
                pass
        return self.paginate_by