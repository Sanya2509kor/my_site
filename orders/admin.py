from django.contrib import admin
from django.http import HttpResponse
from django.template.loader import render_to_string
from orders.models import Order, OrderItem

def print_order(modeladmin, request, queryset):
    # Проверяем, что выбран только один заказ
    if queryset.count() != 1:
        modeladmin.message_user(request, "Пожалуйста, выберите только один заказ для печати.", level='ERROR')
        return
    
    order = queryset.first()
    order_items = OrderItem.objects.filter(order=order)
    
    # Подготавливаем данные для печати
    context = {
        'order': order,
        'order_items': order_items,
        'total_price': sum(item.product_price() for item in order_items),
    }
    
    # Рендерим HTML шаблон
    html = render_to_string('orders/print_order.html', context)
    return HttpResponse(html)
    
    # # Генерация PDF
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = f'attachment; filename="order_{order.id}.pdf"'
    
    # from weasyprint import HTML
    # HTML(string=html).write_pdf(response)
    
    # return response

print_order.short_description = "Печать заказа"




class OrderItemTabulareAdmin(admin.TabularInline):
    model = OrderItem
    fields = "product", "name", "price", "quantity"
    search_fields = (
        "product",
        "name",
    )
    extra = 0

    def product_price(self, instance):
        return instance.product_price()
    product_price.short_description = "Общая цена"
    


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = "order", "product", "name", "price", "quantity"
    search_fields = (
        "order",
        "product",
        "name",
    )
    ordering = ('-id',)
    


class OrderTabulareAdmin(admin.TabularInline):
    model = Order
    fields = (
        "requires_delivery",
        "status",
        "payment_on_get",
        "is_paid",
        "created_timestamp",
    )

    search_fields = (
        "requires_delivery",
        "payment_on_get",
        "is_paid",
        "created_timestamp",
    )
    readonly_fields = ("created_timestamp",)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "requires_delivery",
        "status",
        "payment_on_get",
        "is_paid",
        "created_timestamp",
    )
    list_editable = ('status', 'is_paid')  # если хотите редактировать прямо из списка

    search_fields = (
        "id",
    )
    readonly_fields = ("created_timestamp",)
    list_filter = (
        "requires_delivery",
        "status",
        "payment_on_get",
        "is_paid",
    )
    inlines = (OrderItemTabulareAdmin,)

    ordering = ('-id',)
    actions = [print_order]

    def total_price_display(self, obj):
        return sum(item.product_price() for item in obj.orderitem_set.all())
    total_price_display.short_description = "Общая сумма заказа"