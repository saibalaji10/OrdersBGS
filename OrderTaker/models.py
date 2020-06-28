from django.db import models


class Customer(models.Model):
    name = models.CharField('Customer Name', max_length=100)
    number = models.CharField('Contact Phone', max_length=20)

class Order(models.Model):
    date = models.DateTimeField('Order Date')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField('Product Category', max_length=150, default='x')
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
    product_attribute = models.ManyToManyField(Attribute,through='ProductAttribute')

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.product.name + '-' + self.attribute.name)


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, default=0)
    quantity = models.IntegerField('Item Quantity')

    class Meta:
        verbose_name_plural = "Order Details"
