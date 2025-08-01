from django.contrib import admin
from goods.models import Categories, Products, SubCategories, ProductRelationship
from django import forms


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', ),}
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


    # Добавляем кастомную форму для отображения дополнительных полей
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "to_product":
            kwargs["queryset"] = Products.objects.all().select_related('category')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    # Кастомизация отображения выпадающего списка
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['to_product'].label_from_instance = lambda obj: f"{obj.name} (Цвет: {obj.color}, Размер: {obj.size})"
        return formset






@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    # form = ProductAdminForm
    # prepopulated_fields = {'slug': ('name', )}
    list_display = ['name', 'color', 'size', 'quantity', 'price', 'discount',]
    list_editable = ['discount', 'color', 'size', 'price', 'quantity']
    search_fields = ['name', 'description']
    list_filter = ['discount', 'quantity', 'category', 'color', 'size']
    fields = [
        "name", 
        "category",
        "subcategory",
        # "slug", 
        "description",
        "color",
        "size",
        "image",
        "image_schem",
        ("price", "discount"),
        "quantity",
        ('power', 'bright'),
    ]

    ordering = ('-id',)
    
    inlines = [ProductRelationshipInline]
    
    # Для отображения всех связанных товаров в списке
    def get_queryset(self, request):
        qs = super().get_queryset(request).prefetch_related('related_products')
        # изменил чтобы не показывал товар с 0 количеством
        qs = qs.exclude(quantity=0)
        return qs
    
    # Чтобы избежать проблем с отображением m2m поля
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form
    

