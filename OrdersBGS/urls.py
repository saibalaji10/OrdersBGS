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
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from OrderTaker import views
from OrdersBGS import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('enter/', views.enter, name='enter'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('categories/', views.categories, name='categories'),
    path('category/<int:category_id>/', views.products, name='products'),
    path('add/', views.add_to_cart, name='add'),
    path('cart/', views.cart, name='cart'),
    path('customer_orders/', views.customer_orders, name='customer_orders'),
    path('vieworder/<int:order_id>/', views.order, name='order'),
    path('placeorder/', views.placeorder, name='placeorder'),
    path('<int:order_id>/downloadpdf/', views.downloadpdf, name='downloadpdf'),
    path('OrderTaker/', include('OrderTaker.urls')),
    path(r'admin/', include('massadmin.urls')),
    path('admin/', admin.site.urls),
]
