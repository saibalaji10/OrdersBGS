from django.db import models


# Create your models here.
class Customer(models.Model):
    name = models.CharField('Customer Name', max_length=100)
    number = models.CharField('Contact Phone', max_length=20)

    def __str__(self):
        return self.name

class Order(models.Model):
    date = models.DateTimeField('Order Date')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __int__(self):
        return self.id

class Category(models.Model):
    category = models.CharField('Product Category', max_length=100)

    def __str__(self):
        return self.category

class Attribute(models.Model):
    name = models.CharField('Product Attribute', max_length=150)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField('Product Name', max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_attribute = models.ManyToManyField(Attribute, related_name='product_attribute')
    order = models.ManyToManyField(Order, through='OrderDetails')

    def __str__(self):
        return self.name

class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    quantity = models.IntegerField('Item Quantity')

    def __int__(self):
        return self.id