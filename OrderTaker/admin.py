from .models import Order, OrderDetails, ProductAttribute, Config, Category, Attribute
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import BGSUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = BGSUser
        fields = ('name', 'phone')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = BGSUser
        fields = ('phone', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class BGSUserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('name', 'phone', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'phone', 'password1', 'password2')}
         ),
    )
    search_fields = ('phone',)
    ordering = ('phone',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(BGSUser, BGSUserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)


class ProductResources(resources.ModelResource):

    def before_import_row(self, row, **kwargs):
        categoryobject, created = Category.objects.get_or_create(
            name=row.get('category'))

        attributeobject, created = Attribute.objects.get_or_create(
            name=row.get('attribute')
        )

    category = fields.Field(column_name='category', attribute='category', widget=ForeignKeyWidget(Category, 'name'))
    attribute = fields.Field(column_name='attribute', attribute='attribute', widget=ForeignKeyWidget(Attribute, 'name'))

    product = fields.Field(column_name='product', attribute='product', )

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
    list_display = ('id', 'name')


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
admin.site.register(Config, ConfigAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Attribute, AttributeAdmin)
