from django.contrib import admin

from .models import Product, Order, Category, Attribute, Customer, OrderDetails


class ProductAdmin(admin.ModelAdmin):
    # ...
    list_display = ('name', 'category', 'id')


class OrderAdmin(admin.ModelAdmin):
    # ...
    list_display = ('date', 'customer', 'id')


class CategoryAdmin(admin.ModelAdmin):
    # ...
    list_display = ('category', 'id')


class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'attribute', 'quantity')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'id')


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(OrderDetails, OrderDetailsAdmin)
admin.site.register(Customer, CustomerAdmin)