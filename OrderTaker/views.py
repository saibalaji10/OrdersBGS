from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Order, Customer, OrderDetails, ProductAttribute, Config
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Sum
from .Utilities.orderprinter import OrderPrinter
from django.http import HttpResponse, Http404
import datetime


def addtocart(request):
    page = "1"
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

    # print('order_id:', request.session['order_id'])
    # print('customer_id', request.session['customer_id'])
    success = False
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
                    success = True
            except Exception as e:
                messages.error(request, 'Error adding item!', extra_tags='danger')
        if key == "current_page" and value:
            page = value
    if success:
        messages.success(request, 'Your item added to cart successfully!')
    request.session['customer_id'] = cust.id
    request.session['order_id'] = cust_order.id
    return HttpResponseRedirect(reverse('home') + '?page=' + str(page))

def cart(request):
    context = {}
    if 'customer_id' in request.session:
        order_items = OrderDetails.objects.filter(order_id=request.session['order_id'])
        context['order_items'] = order_items
        return render(request, 'OrderTaker/cart.html', context)
    return HttpResponseRedirect(reverse('home'))

def deleteitem(request, order_item_id):
    OrderDetails.objects.filter(pk=order_item_id).delete()
    return HttpResponseRedirect(reverse('cart'))

def placeorder(request):
    context = {}

    if request.method == 'POST':
        for key, value in request.POST.items():
            if key[:9] == "orderitem" and value:
                od_id = key[9:]
                try:
                    if int(value) != 0:
                        od = OrderDetails.objects.filter(pk=od_id).update(quantity=value)
                except Exception as e:
                    print(e)

        if 'order_id' in request.session:
            order_items = OrderDetails.objects.filter(order_id=request.session['order_id'])
            order_printer = OrderPrinter(order_items)
            print('Generating Order pdf')
            order_printer.execute_action()

        context['order_message'] = Config.objects.get(property__iexact='Message')
        context['order_id'] = request.session['order_id']
        context['customer'] = Customer.objects.filter(customers__id=request.session["customer_id"])
        request.session.flush()
        return render(request, 'OrderTaker/thankyou.html', context)

    request.session.flush()
    return HttpResponseRedirect(reverse('home'))

def downloadpdf(request, order_id):
    order_items = OrderDetails.objects.filter(order_id=order_id)
    order_printer = OrderPrinter(order_items)
    pdf_content = order_printer.download_pdf()
    file_name = 'Order_' + str(order_items[0].order.id) + '.pdf'
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + file_name
    return response

def home(request):
    if 'customer_id' in request.session:
        print("Logged in")
        return categories(request)
    print("Log in failed")
    return render(request, 'OrderTaker/userdetails.html', {})

def enter(request):
    if request.method == 'POST':
        username = request.POST.get('username', 'user')
        number = request.POST.get('phonenumber', '9876543210')
        customer = Customer(
            name=username, number=number
        )

        customer_order = Order(
            customer=customer
        )
        customer.save()
        customer_order.save()

        request.session['customer_id'] = customer.id
        request.session['order_id'] = customer_order.id
        return categories(request)

    return home(request)
# Create your views here.
def categories(request):
    context = {}
    config_list = Config.objects.all()
    mode = config_list.get(property__iexact='Control').value
    state = config_list.get(property__iexact='State').value

    if 'manual' == str(mode).lower():
        if 'off' == str(state).lower():
            print('Website state is off, not rendering orders page')
            return render(request, 'OrderTaker/willbeback.html', {mode: 'manual'})
        else:
            print('Website state is on, rendering orders page')

    elif 'auto' == str(mode).lower():
        start = config_list.get(property__iexact='Start').value
        end = config_list.get(property__iexact='Stop').value
        start_time_object = datetime.datetime.strptime(start, '%H:%M').time()
        end_time_object = datetime.datetime.strptime(end, '%H:%M').time()

        current_time = datetime.datetime.now().time()
        if current_time >= start_time_object and current_time <= end_time_object:
            print('Time check complete, Rendering home page for orders')
        else:
            print('Time check complete, Website is not turned on')
            return render(request, 'OrderTaker/willbeback.html', {'mode': 'auto', 'start': start, 'end': end})

    # In case of rendering orders page, getting data from models
    pa_list = ProductAttribute.objects.filter(isVisible__exact='show')

    product_list = ProductAttribute.objects.filter(isVisible__exact='show').distinct('product')

    category_list = ProductAttribute.objects.filter(isVisible__exact='show').distinct('category')

    attribute_list = ProductAttribute.objects.filter(isVisible__exact='show').distinct('attribute')

    if 'order_id' in request.session:
        co_list = ProductAttribute.objects.filter(productattributes__order_id=request.session['order_id'])
        cat_count = list(ProductAttribute.objects.
                         filter(productattributes__order_id=request.session['order_id']).
                         annotate(quantity=Sum('productattributes__quantity')).
                         values('id', 'category', 'quantity'))

        context['co_list'] = co_list
        context['cat_count'] = cat_count
        print(cat_count)
    page = request.GET.get('page', 1)

    paginator = Paginator(category_list, 10)

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

def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('home'))
