from django.contrib import admin
from goods.models import Categories, Products, SubCategories, ProductRelationship


# admin.site.register(Categories)
# admin.site.register(Products)



@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ['name', ]


@admin.register(SubCategories)
class SubCategoriesAdmin(admin.ModelAdmin):  # Изменил имя класса для ясности
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name',]

class ProductRelationshipInline(admin.TabularInline):
    model = ProductRelationship
    fk_name = 'from_product'
    extra = 1
    verbose_name = 'Сопутствующий товар'
    verbose_name_plural = 'Сопутствующие товары'


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ['name', 'quantity', 'price', 'discount']
    list_editable = ['discount', ]
    search_fields = ['name', 'description']
    list_filter = ['discount', 'quantity', 'category']
    fields = [
        "name", 
        "category",
        "subcategory",
        "slug", 
        "description",
        "image",
        ("price", "discount"),
        "quantity",
    ]
    inlines = [ProductRelationshipInline]
    
    # Для отображения всех связанных товаров в списке
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('related_products')

    
    # Чтобы избежать проблем с отображением m2m поля
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form