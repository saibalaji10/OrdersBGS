from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import Product, Order, Category, Attribute, Customer, OrderDetails, ProductAttribute
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


class ProductResources(resources.ModelResource):

    def before_import_row(self, row, **kwargs):
        categoryobject, created = Category.objects.get_or_create(
            name=row.get('category'))

        Product.objects.get_or_create(
            name=row.get('product'),
            category=categoryobject
        )

        Attribute.objects.get_or_create(
            name=row.get('attribute')
        )

    product = fields.Field(column_name='product', attribute='product',
                           widget=ForeignKeyWidget(Product, 'name'))

    attribute = fields.Field(column_name='attribute', attribute='attribute',
                             widget=ForeignKeyWidget(Attribute, field='name'));

    class Meta:
        model = ProductAttribute
        skip_unchanged = True
        report_skipped = True
        exclude = ('id', 'category')
        import_id_fields = ('product', 'attribute')


class ProductAdmin(admin.ModelAdmin):
    # ...

    # inlines = [ProductInline, ]
    list_display = ('name', 'category',)
    filter_horizontal = ('product_attribute',)


class OrderAdmin(admin.ModelAdmin):
    # ...
    list_display = ('date', 'customer', 'id')


class CategoryAdmin(admin.ModelAdmin):
    # ...
    list_display = ('name', 'id')
    inlines = [ProductInline, ]


class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


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
    list_display = ('id', 'categories', 'product', 'attribute',)

    list_filter = ('product', 'attribute',)

    resource_class = ProductResources

    def categories(self, obj):
        return obj.product.category.name


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(OrderDetails, OrderDetailsAdmin)
admin.site.register(Customer, CustomerAdmin)

admin.site.register(ProductAttribute, ProductAttributeAdmin)
