from django.contrib import admin

from .models import Item, Order

class ItemAdmin(admin.ModelAdmin):
    # ...
    list_display = ('item_id', 'item_name','item_type')


class OrderAdmin(admin.ModelAdmin):
    # ...
    list_display = ('order_id', 'item_id', 'quantity')


admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)