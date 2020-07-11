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


class Category(models.Model):
    name = models.CharField('Product Category', max_length=150)
    isVisible = models.CharField(max_length=256, choices=[('show', 'show'), ('hide', 'hide')], default='show')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Attribute(models.Model):
    name = models.CharField('Product Attribute', max_length=150)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('Product Name', max_length=200)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    product_attribute = models.ManyToManyField(Attribute, through='ProductAttribute')

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, related_name='products', on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, related_name='attributes', on_delete=models.CASCADE)
    isVisible = models.CharField(max_length=256, choices=[('show', 'show'), ('hide', 'hide')], default='show')

    def __str__(self):
        return str(self.product.name + '-' + self.attribute.name)

    class Meta:
        unique_together = ('product', 'attribute',)


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_attribute = models.ForeignKey(ProductAttribute, related_name='productattributes', on_delete=models.CASCADE)
    quantity = models.IntegerField('Item Quantity')

    class Meta:
        verbose_name_plural = "Order Details"


class Config(models.Model):
    property = models.CharField('Property', max_length=20, unique=True, null=False)
    value = models.CharField('Value', max_length=300, null=False)
    property_description = models.CharField('Property Description', max_length=250, default= '', null=False)
    class Meta:
        verbose_name_plural = "Configurations"
