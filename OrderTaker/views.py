from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Order, Category, Attribute, Customer, OrderDetails, ProductAttribute


# Create your views here.
def index(request):
    category_list = Category.objects.order_by('name')
    product_list = Product.objects.order_by('name')
    attribute_list = Attribute.objects.order_by('name')
    pa_list = ProductAttribute.objects.all()

    print(product_list)
    print(category_list)
    print(attribute_list)
    print(pa_list)
    context = {
        'category_list': category_list,
        'product_list': product_list,
        'attribute_list': attribute_list,
        'pa_list': pa_list
    }
    return render(request, 'OrderTaker/index.html', context)
