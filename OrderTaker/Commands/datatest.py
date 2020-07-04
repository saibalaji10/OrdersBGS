from OrderTaker.models import *
from django.db.models import Sum, F

category_list = Category.objects.all()
attribute_list = Attribute.objects.all()
product_list = Product.objects.all()
pa_list = ProductAttribute.objects.all()
od_list = OrderDetails.objects.all()

cust = Customer.objects.all()

Customer.objects.all()

Category.objects.filter(products__products__productattributes__order_id=1, id=2)

Category.objects.filter(products__products__productattributes__order_id=1)

x = Category.objects. \
    filter(products__products__productattributes__order_id=1). \
    annotate(quantity=Sum('products__products__productattributes__quantity')). \
    values('name', 'quantity')
print(list(x))

x = Category.objects. \
    filter(products__products__productattributes__order_id=1). \
    annotate(quantity=Sum('products__products__productattributes__quantity')). \
    values('id', 'name', 'quantity')
print(list(x))

x = Category.objects.annotate(quantity=Sum('products__products__productattributes__quantity')).values('name',
                                                                                                      'quantity')
print(list(x))
