from django.db import models
from django.utils import timezone


class Customer(models.Model):
    name = models.CharField('Customer Name', max_length=100)
    number = models.CharField('Contact Phone', max_length=20)

    def __str__(self):
        return self.name


class Order(models.Model):
    date = models.DateTimeField('Order Date', default=timezone.now)
    customer = models.ForeignKey(Customer, related_name='customers', on_delete=models.CASCADE)
    additional_comments = models.TextField(null=True, blank=True)

    def __int__(self):
        return self.id

class ProductAttribute(models.Model):
    category = models.CharField('Category', max_length=150)
    product = models.CharField('Product', max_length=200)
    attribute = models.CharField('Attribute', max_length=150)
    isVisible = models.CharField(max_length=256, choices=[('show', 'show'), ('hide', 'hide')], default='show')

    def __str__(self):
        return str(self.product + '-' + self.attribute)

    class Meta:
        unique_together = ('category', 'product', 'attribute',)


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_attribute = models.ForeignKey(ProductAttribute, related_name='productattributes', on_delete=models.CASCADE)
    quantity = models.IntegerField('Item Quantity')

    class Meta:
        verbose_name_plural = "Order Details"


class Config(models.Model):
    property = models.CharField('Property', max_length=20, unique=True, null=False)
    value = models.CharField('Value', max_length=500, null=False)
    property_description = models.CharField('Property Description', max_length=250, default= '', null=False)
    format = models.CharField('Value Format', max_length=50, default='', null=False)
    class Meta:
        verbose_name_plural = "Configurations"
