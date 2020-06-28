from django.shortcuts import render
from .models import Product, Category, Attribute, ProductAttribute
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    category_list = Category.objects.order_by('name')
    page = request.GET.get('page', 1)

    paginator = Paginator(category_list, 5)

    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)

    context = {
        'category_list': categories,
    }
    return render(request, 'OrderTaker/index.html', context)
