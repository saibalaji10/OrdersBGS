"""OrdersBGS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from OrderTaker import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.addtocart, name='add'),
    path('cart/', views.cart, name='cart'),
    path('user/', views.userdetails, name='userdetails'),
    path('placeorder/', views.placeorder, name='placeorder'),
    path('downloadpdf/', views.downloadpdf, name='downloadpdf'),
    path('completeorder/', views.completeorder, name='completeorder'),
    path('OrderTaker/', include('OrderTaker.urls')),
    path('admin/', admin.site.urls),
]
