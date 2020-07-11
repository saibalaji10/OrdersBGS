from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:order_item_id>/deleteitem/',views.deleteitem, name='deleteitem')
]
