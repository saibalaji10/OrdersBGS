from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:order_item_id>/deleteitem/',views.deleteitem, name='deleteitem')
]
