from django.urls import path
from examples import views 


app_name = 'examples'

urlpatterns = [
    path('', views.ExamplesView.as_view(), name='examples'),
]
