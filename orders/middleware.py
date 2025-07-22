# orders/middleware.py
from django.utils import timezone
from .models import AdminNotification, Order

class NewOrderNotificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.user.is_staff and request.path.startswith('/admin/'):
            notification, _ = AdminNotification.objects.get_or_create(pk=1)
            new_orders = Order.objects.filter(created_timestamp__gt=notification.last_update)
            
            if new_orders.exists():
                notification.last_checked_order = new_orders.latest('created_timestamp')
                notification.save()
                request.session['has_new_orders'] = True
        
        return response