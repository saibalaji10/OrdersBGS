from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import Order, Customer, OrderDetails, ProductAttribute, Config
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget


#
class ProductResources(resources.ModelResource):

    def before_import_row(self, row, **kwargs):
        ProductAttribute.objects.get_or_create(
            product=row.get('product'),
            category=row.get('category'),
            attribute=row.get('attribute')
        )

    class Meta:
        model = ProductAttribute
        skip_unchanged = True
        report_skipped = True
        exclude = ('id', 'category')
        import_id_fields = ('product', 'attribute')

class OrderAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id', 'customer', 'date')
    search_fields = ['customer__name', 'id']


class ConfigAdmin(admin.ModelAdmin):
    # ...
    list_display = ('property', 'value', 'property_description', 'format')
    search_fields = ['property', 'value', 'property_description']

    def has_delete_permission(self, request, obj=None):
        return False


class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_attribute', 'quantity')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'id')


class CategoryFilter(SimpleListFilter):
    title = 'Category'
    parameter_name = 'Categories name'

    def lookups(self, request, model_admin):
        categories = tuple(list(set([c.product.category.name for c in model_admin.model.objects.all()])))
        return (categories, categories)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(product__category__name=self.value())


class ProductAttributeAdmin(ImportExportModelAdmin):
    list_display = ('id', 'category', 'product', 'attribute', 'isVisible')

    list_filter = ('category', 'attribute', 'product')

    # resource_class = ProductResources
    actions = ['hide_selected_items', 'show_selected_items']

    def hide_selected_items(modeladmin, request, queryset):
        queryset.update(isVisible='hide')

    hide_selected_items.short_description = "Hide Selected Items"

    def show_selected_items(modeladmin, request, queryset):
        queryset.update(isVisible='show')

    def categories(self, obj):
        return obj.product.category.name


admin.site.site_header = 'Bombay General Stores Admin'
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetails, OrderDetailsAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Config, ConfigAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
