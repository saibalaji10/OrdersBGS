from django.shortcuts import render
from .models import Product, Category, Attribute, ProductAttribute


def index(request):
    pa_list = ProductAttribute.objects.all()

    distinct_prod_list = pa_list.values_list('product').distinct()
    product_list = Product.objects.filter(id__in=distinct_prod_list).order_by('name')

    distinct_category_list = Product.objects.filter(id__in=distinct_prod_list).values_list('category').distinct()
    category_list = Category.objects.filter(id__in=distinct_category_list).order_by('name')

    attribute_list = Attribute.objects.order_by('name')

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


def index2(request):
    pa_list = ProductAttribute.objects.all()

    distinct_prod_list = pa_list.values_list('product').distinct()
    product_list = Product.objects.filter(id__in=distinct_prod_list).order_by('name')

    distinct_category_list = Product.objects.filter(id__in=distinct_prod_list).values_list('category').distinct()
    category_list = Category.objects.filter(id__in=distinct_category_list).order_by('name')

    attribute_list = Attribute.objects.order_by('name')

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
    return render(request, 'OrderTaker/index2.html', context)
