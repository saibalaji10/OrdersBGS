from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Order, Category, Attribute, Customer, OrderDetails, ProductAttribute


# Create your views here.
def index(request):
    pa_list = ProductAttribute.objects.all()

    distinct_prod_list = pa_list.values_list('product').distinct()
    product_list = Product.objects.filter(id__in=distinct_prod_list).order_by('name')

    distinct_category_list = Product.objects.filter(id__in=distinct_prod_list).values_list('category').distinct()
    category_list = Category.objects.filter(id__in=distinct_category_list).order_by('name')

    attribute_list = Attribute.objects.order_by('name')

    context = {
        'category_list': category_list,
        'product_list': product_list,
        'attribute_list': attribute_list,
        'pa_list': pa_list
    }
    return render(request, 'OrderTaker/index.html', context)


def addtocart(request):
    # if request.session.get('first_time',True):
    cust = Customer(
        name="user"
    )
    # if request.session.get('customer_id', cust.id):
    cust.save()
    cust_order = Order(
        customer=cust
    )
    # if request.session.get('order_id', cust_order.id):
    cust_order.save()
    for key, value in request.POST.items():
        if key[:12] == "ProdQuantity":
            pa_id = key[12:]
            OrderDetails.objects.create(
                product_attribute=ProductAttribute.objects.get(pk=pa_id),
                quantity=value,
                order=cust_order
            )
        # request.session['order_id'] = cust_order.id
    # request.session['customer_id'] = cust.id

    return HttpResponse("Added!")
