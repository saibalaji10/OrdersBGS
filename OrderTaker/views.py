from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Product, Order, Category, Attribute, Customer, OrderDetails, ProductAttribute
from django.urls import reverse


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
        'pa_list': pa_list,
        'message': request.session['message'] if 'message' in request.session else None
    }
    return render(request, 'OrderTaker/index.html', context)


def addtocart(request):
    try:
        # Get Customer object for given session
        cust = Customer.objects.get(
            pk=request.session['customer_id']
        )
        # Get Order object for given session
        cust_order = Order.objects.get(
            pk=request.session['order_id'],
            customer=cust
        )
        print('Next time')
    except (ObjectDoesNotExist, KeyError) as e:
        # create customer object
        print('First Time')
        cust = Customer(
            name="user1"
        )
        # create order object
        cust_order = Order(
            customer=cust
        )
        cust.save()
        cust_order.save()

    print("CustomerID:", cust.id)
    print("OrderID", cust_order.id)

    # If adding to cart for the first time

    for key, value in request.POST.items():
        print("Key:", key)
        print("Value:", value)

    # print('order_id:', request.session['order_id'])
    # print('customer_id', request.session['customer_id'])

    message = 'Added to Cart!'
    for key, value in request.POST.items():
        if key[:12] == "ProdQuantity" and int(value) > 0:
            pa_id = key[12:]
            try:
                od = OrderDetails.objects.get_or_create(
                    product_attribute=ProductAttribute.objects.get(pk=pa_id),
                    quantity=value,
                    order=cust_order
                )
            except:
                message = 'Error!'

    request.session['message'] = message
    request.session['customer_id'] = cust.id
    request.session['order_id'] = cust_order.id

    return HttpResponseRedirect(reverse('index'))
