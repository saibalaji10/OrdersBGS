from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .forms import RegisterForm
from .models import Order, OrderDetails, ProductAttribute, Config, BGSUser
from django.urls import reverse
from django.contrib import messages, auth
from .Utilities.orderprinter import OrderPrinter
from django.http import HttpResponse
import datetime


def register(request):
    template = 'OrderTaker/register.html'

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if BGSUser.objects.filter(phone=form.cleaned_data['phone']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Account already exists. Please sign in to your account. If not, use a different '
                                     'phone number '
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Passwords do not match.'
                })
            else:
                user = BGSUser.objects.create_user(
                    form.cleaned_data['phone'],
                    form.cleaned_data['password']
                )
                user.name = form.cleaned_data['name']
                user.save()

                auth.login(request, user)

                return HttpResponseRedirect(reverse('categories'))

    else:
        form = RegisterForm()

    return render(request, template, {'form': form})


def home(request):
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
        if start_time_object <= current_time <= end_time_object:
            print('Time check complete, Rendering home page for orders')
        else:
            print('Time check complete, Website is not turned on')
            return render(request, 'OrderTaker/willbeback.html', {'mode': 'auto', 'start': start, 'end': end})

    if request.user.is_authenticated:
        print("Logged in as:" + request.user.name)
        return categories(request)

    print("Not logged in..")
    return HttpResponseRedirect(reverse('login'))


def enter(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']
        user = authenticate(request, username=phone, password=password)
        if user is not None:
            auth.login(request, user)
            customer_order, is_created = Order.objects.get_or_create(
                customer=request.user,
                cart=True,
            )
            if is_created:
                customer_order.save()
            messages.success(request, f' Welcome {request.user.name} !!')
            return redirect('categories')
        else:
            messages.info(request, 'Account does not exist please sign in..')

    return render(request, 'OrderTaker/login.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('categories')
    return render(request, 'OrderTaker/login.html')


# Create your views here.
def products(request, category_id):
    context = {}
    product_list_full = list(
        ProductAttribute.objects.filter(category_id__exact=category_id).values('product',
                                                                               'id',
                                                                               'category__name',
                                                                               'attribute__name'))
    category_id_arg = category_id
    if len(product_list_full) <= 0:
        return

    category_name = product_list_full[0]['category__name']

    result_product_list = []
    for product_item in product_list_full:
        if not any(d['product_name'] == product_item['product'] for d in result_product_list):
            product_dict = {'product_name': product_item['product'], 'product_attribute_list': []}
            product_attribute_dict = {'product_id': product_item['id'], 'attribute': product_item['attribute__name']}
            product_dict['product_attribute_list'].append(product_attribute_dict)
            result_product_list.append(product_dict)

        else:
            for product_dict in result_product_list:
                if product_dict.get('product_name', '') == product_item['product']:
                    product_attribute_dict = {'product_id': product_item['id'],
                                              'attribute': product_item['attribute__name']}
                    product_dict['product_attribute_list'].append(product_attribute_dict)

    context['product_list'] = result_product_list
    context['category'] = category_name
    context['category_id'] = category_id_arg

    return render(request, 'OrderTaker/products.html', context)


# Create your views here.
def categories(request):
    context = {}

    category_list_full = list(
        ProductAttribute.objects.filter(isVisible__iexact='show').values('category__id',
                                                                         'category__name',
                                                                         ))
    result_category_list = []
    for indiv_category in category_list_full:
        if not any(d['category_id'] == indiv_category['category__id'] for d in result_category_list):

            indiv_category_dict = {}
            category_name = indiv_category['category__name']
            if category_name == '-':
                continue
            category_id = indiv_category['category__id']
            indiv_category_dict['category_name'] = category_name
            indiv_category_dict['category_id'] = category_id
            result_category_list.append(indiv_category_dict)

    sorted_category_list = sorted(result_category_list, key=lambda k: k['category_name'])

    context['category_list'] = sorted_category_list
    context['message'] = request.session['message'] if 'message' in request.session else None

    return render(request, 'OrderTaker/categories.html', context)


def logout(request):
    request.session.flush()
    auth.logout(request)
    return HttpResponseRedirect(reverse('home'))


def add_to_cart(request):
    page = -1

    print(request)
    # Get Customer object for given session
    cust = request.user
    # Get Order object for given session

    customer_order, is_created = Order.objects.get_or_create(
        customer=request.user,
        cart=True
    )

    if is_created:
        customer_order.save()

    success = False
    for key, value in request.POST.items():
        print(key)
        print(value)
        if key == "category" and value:
            page = value

        if page == -1:
            return redirect('categories')
        if key[:12] == "ProdQuantity" and value:
            pa_id = key[12:]
            print(pa_id)
            try:
                if int(value) != 0:
                    od, created = OrderDetails.objects.update_or_create(
                        product_attribute=ProductAttribute.objects.get(pk=pa_id),
                        order=customer_order,
                        defaults={'quantity': int(value)},
                    )
                    success = True
            except Exception as e:
                print(e)
                messages.error(request, 'Error adding item!', extra_tags='danger')

    if success:
        messages.success(request, 'Your item added to cart successfully!')
    return redirect('products', category_id=page)


@login_required
def cart(request):
    context = {}
    customer_order, is_created = Order.objects.get_or_create(customer_id=request.user.id, cart=True)
    order_items = OrderDetails.objects.filter(order_id=customer_order.id)
    context['order_items'] = order_items
    return render(request, 'OrderTaker/cart.html', context)


def deleteitem(request, order_item_id):
    OrderDetails.objects.filter(pk=order_item_id).delete()
    return HttpResponseRedirect(reverse('cart'))


@login_required
def customer_orders(request):
    context = {}
    order_list = list(Order.objects.filter(customer_id__exact=request.user.id, cart__exact=False).values('id',
                                                                                                         'date',
                                                                                                         'additional_comments',
                                                                                                         'cart'
                                                                                                         ))
    context['orders'] = order_list
    print(order_list)
    return render(request, 'OrderTaker/customerOrders.html', context)


@login_required
def order(request, order_id):
    context = {}
    order_items = list(OrderDetails.objects.filter(order_id=order_id))
    context['order_items'] = order_items
    return render(request, 'OrderTaker/order.html', context)


def placeorder(request):
    context = {}

    if request.method == 'POST':
        customer_order, is_created = Order.objects.get_or_create(customer_id=request.user.id, cart=True)
        for key, value in request.POST.items():
            if key[:9] == "orderitem" and value:
                od_id = key[9:]
                try:
                    if int(value) != 0:
                        OrderDetails.objects.filter(pk=od_id).update(quantity=value)
                except Exception as e:
                    print(e)

            if key == 'commentsTextArea' and value:
                try:
                    Order.objects.filter(pk=customer_order.id).update(additional_comments=value,
                                                                      cart=False)
                except Exception as e:
                    print(e)
            else:
                try:
                    Order.objects.filter(pk=customer_order.id).update(cart=False)
                except Exception as e:
                    print(e)

        order_items = OrderDetails.objects.filter(order_id=customer_order.id)
        order_printer = OrderPrinter(order_items)
        print('Generating Order pdf')
        order_printer.execute_action()

        context['order_message'] = Config.objects.get(property__iexact='Message')
        context['order_id'] = customer_order.id
        context['customer'] = request.user.name
        new_current_order = Order(customer=request.user, cart=True)
        new_current_order.save()
        return render(request, 'OrderTaker/thankyou.html', context)

    return HttpResponseRedirect(reverse('home'))


def downloadpdf(request, order_id):
    order_items = OrderDetails.objects.filter(order_id=order_id)
    order_printer = OrderPrinter(order_items)
    pdf_content = order_printer.download_pdf()
    file_name = 'Order_' + str(order_items[0].order.id) + '.pdf'
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + file_name
    return response
