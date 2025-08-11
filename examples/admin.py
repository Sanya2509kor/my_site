from django.contrib import admin
from django.utils.html import format_html
from examples.models import Examples, ListImages


class ListImagesInline(admin.TabularInline):
    model = ListImages
    extra = 1
    fields = ('image', 'image_preview')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.image.url)
        return "Нет изображения"
    image_preview.short_description = "Превью"


@admin.register(Examples)
class ExamplesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description_short', 'images_count')
    list_display_links = ('name',)
    list_filter = ('name',)
    search_fields = ('name', 'description')
    fields = ('name', 'description')  # Убрано поле image, так как оно в другой модели
    inlines = [ListImagesInline]

    def description_short(self, obj):
        return f"{obj.description[:100]}..." if obj.description else ''
    description_short.short_description = 'Описание'

    def images_count(self, obj):
        return obj.images.count()
    images_count.short_description = 'Кол-во изображений'


@admin.register(ListImages)
class ListImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_link', 'image_preview')
    list_filter = ('product',)
    readonly_fields = ('image_preview',)

    def product_link(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html
        url = reverse('admin:examples_examples_change', args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', url, obj.product.name)
    product_link.short_description = 'Пример работы'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.image.url)
        return "Нет изображения"
    image_preview.short_description = 'Превью'