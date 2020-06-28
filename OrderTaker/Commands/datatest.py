from OrderTaker.models import *

category_list = Category.objects.all()
attribute_list = Attribute.objects.all()
product_list = Product.objects.all()
pa_list = ProductAttribute.objects.all()
od_list = OrderDetails.objects.all()

cust = Customer.objects.all()

Customer.objects.all()
