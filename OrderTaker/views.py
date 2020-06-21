from django.shortcuts import render
from .models import Category, Product

# Create your views here.
def index(request):
    category_list = Category.objects.order_by('category')
    product_list = Product.objects.order_by('name')
    print(product_list)
    print(category_list)
    context = {'category_list' : category_list, 'product_list' : product_list }
    return render(request, 'OrderTaker/index.html', context)