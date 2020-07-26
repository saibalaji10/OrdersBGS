from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import Order, Customer, OrderDetails, ProductAttribute, Config, Category, Attribute
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget


#
class ProductResources(resources.ModelResource):

    def before_import_row(self, row, **kwargs):
        categoryobject, created = Category.objects.get_or_create(
            name=row.get('category'))

        attributeobject, created = Attribute.objects.get_or_create(
            name=row.get('attribute')
        )
    category = fields.Field(column_name='category', attribute='category', widget=ForeignKeyWidget(Category, 'name'))
    attribute = fields.Field(column_name='attribute', attribute='attribute', widget=ForeignKeyWidget(Attribute, 'name'))

    product = fields.Field(column_name='product', attribute='product',)

    class Meta:
        model = ProductAttribute
        skip_unchanged = True
        report_skipped = True
        exclude = ('id', 'category')
        import_id_fields = ('product', 'attribute')

class ConfigResources(resources.ModelResource):

    def before_import_row(self, row, **kwargs):
        Config.objects.get_or_create(
            property=row.get('property'),
            value=row.get('value'),
            property_description=row.get('property_description'),
            format=row.get('format')
        )

    class Meta:
        model = Config
        skip_unchanged = True
        report_skipped = True
        exclude = ('id')

class OrderAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id', 'customer', 'date')
    search_fields = ['customer__name', 'id']


class ConfigAdmin(ImportExportModelAdmin):
    # ...
    list_display = ('property', 'value', 'property_description', 'format')
    search_fields = ['property', 'value', 'property_description']

    def has_delete_permission(self, request, obj=None):
        return False


class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_attribute', 'quantity')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'id')

class AttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class ProductAttributeAdmin(ImportExportModelAdmin):
    list_display = ('id', 'category', 'product', 'attribute', 'isVisible')

    list_filter = ('category', 'attribute', 'product')

    resource_class = ProductResources
    actions = ['hide_selected_items', 'show_selected_items']

    def hide_selected_items(modeladmin, request, queryset):
        queryset.update(isVisible='hide')

    hide_selected_items.short_description = "Hide Selected Items"

    def show_selected_items(modeladmin, request, queryset):
        queryset.update(isVisible='show')


admin.site.site_header = 'Bombay General Stores Admin'
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetails, OrderDetailsAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Config, ConfigAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Attribute, AttributeAdmin)
