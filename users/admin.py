from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from carts.admin import CartTabAdmin
from orders.admin import OrderTabulareAdmin
from users.models import User


# admin.site.register(User)

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['first_name', 'last_name', 'email', 'username']
    search_fields = ['first_name', 'last_name', 'email', 'username']

    inlines = [CartTabAdmin, OrderTabulareAdmin]
