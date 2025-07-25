from django.urls import path
from django.http import JsonResponse

from .models import SubCategories
from goods import views 


app_name = 'goods'


# def get_subcategories(request):
#     category_id = request.GET.get('category_id')
#     if category_id:
#         subcategories = SubCategories.objects.filter(category_id=category_id).values('id', 'name')
#         return JsonResponse(list(subcategories), safe=False)
#     return JsonResponse([], safe=False)



urlpatterns = [
    # path('admin/get_subcategories/', get_subcategories, name='get_subcategories'),
    path('search/', views.CatalogView.as_view(), name='search'),
    path('<slug:category_slug>/', views.CatalogView.as_view(), name='index'),
    path('product/<slug:product_slug>/', views.ProductView.as_view(), name='product'),
    path('<slug:category_slug>/<slug:subcategory_slug>/', views.SubCatalogView.as_view(), name='index'),

]