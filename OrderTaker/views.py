from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Product, Order, Category, Attribute, Customer, OrderDetails, ProductAttribute
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core import serializers
from django.db.models import Sum


# Create your views here.
def index(request):
    context = {}
    pa_list = ProductAttribute.objects.all()

    distinct_prod_list = pa_list.values_list('product').distinct()
    product_list = Product.objects.filter(id__in=distinct_prod_list).order_by('name')

    distinct_category_list = Product.objects.filter(id__in=distinct_prod_list).values_list('category').distinct()
    category_list = Category.objects.filter(id__in=distinct_category_list).order_by('name')

    attribute_list = Attribute.objects.order_by('name')

    if 'order_id' in request.session:
        co_list = Category.objects.filter(
            products__products__productattributes__order_id=request.session['order_id'])
        cat_count = list(Category.objects.
                         filter(products__products__productattributes__order_id=request.session['order_id']).
                         annotate(quantity=Sum('products__products__productattributes__quantity')).
                         values('id', 'name', 'quantity'))
        context['co_list'] = serializers.serialize("json", co_list)
        context['cat_count'] = cat_count

    page = request.GET.get('page', 1)

    paginator = Paginator(category_list, 5)

    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)

    context['category_list'] = categories
    context['product_list'] = product_list
    context['attribute_list'] = attribute_list
    context['pa_list'] = pa_list
    context['message'] = request.session['message'] if 'message' in request.session else None

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
        if key[:12] == "ProdQuantity" and value:
            pa_id = key[12:]
            try:
                if int(value) != 0:
                    od, created = OrderDetails.objects.update_or_create(
                        product_attribute=ProductAttribute.objects.get(pk=pa_id),
                        order=cust_order,
                        defaults={'quantity': int(value)},
                    )
                    messages.success(request, 'Your item added to cart successfully!')
            except Exception as e:
                messages.error(request, 'Error adding item!', extra_tags='danger')
                print(e)

    # request.session['message'] = message
    request.session['customer_id'] = cust.id
    request.session['order_id'] = cust_order.id

    return HttpResponseRedirect(reverse('index'))


def cart(request):
    order_items = OrderDetails.objects.filter(order_id=request.session['order_id'])
    print(order_items)
    context = {
        'order_items': order_items,
    }
    return render(request, 'OrderTaker/cart.html', context)


def userdetails(request):
    context = {}

    for key, value in request.POST.items():
        print("Key:", key)
        print("Value:", value)

    for key, value in request.POST.items():
        if key[:9] == "orderitem" and value:
            od_id = key[9:]
            try:
                if int(value) != 0:
                    od = OrderDetails.objects.filter(pk=od_id).update(quantity=value)
            except Exception as e:
                print(e)

    user = Customer.objects.get(customers__id=request.session["customer_id"])

    context['user'] = user
    return render(request, 'OrderTaker/userdetails.html', context)


def placeorder(request):
    for key, value in request.POST.items():
        print("Key:", key)
        print("Value:", value)

    if request.method == 'POST':
        username = request.POST.get('username', 'user')
        number = request.POST.get('phonenumber', '9876543210')
        user = Customer.objects.filter(
            customers__id=request.session["customer_id"]
        ).update(name=username, number=number)
        messages.success(request, "Order placed successfully!")

    request.session.flush()
    return HttpResponseRedirect(reverse('index'))
