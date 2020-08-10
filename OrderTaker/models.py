from django.db import models
from django.utils import timezone

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class BGSUserManager(BaseUserManager):
    def create_user(self, phone, name, password=None):
        """
        Creates and saves a User with the given phone, date of
        birth and password.
        """
        if not phone:
            raise ValueError('Users must have an phone number')

        user = self.model(
            phone=phone,
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, name, password=None):
        """
        Creates and saves a superuser with the given phone, date of
        birth and password.
        """
        user = self.create_user(
            phone=phone,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class BGSUser(AbstractBaseUser):
    phone = models.CharField(
        verbose_name='phone number',
        max_length=10,
        unique=True,
        default=''
    )
    name = models.CharField(max_length=50, default='', null=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = BGSUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Order(models.Model):
    date = models.DateTimeField('Order Date', default=timezone.now)
    customer = models.ForeignKey(BGSUser, related_name='users', on_delete=models.CASCADE)
    additional_comments = models.TextField(null=True, blank=True)
    cart = models.BooleanField(default=False, null=True)

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


class ProductAttribute(models.Model):
    category = models.ForeignKey(Category, related_name='categories', on_delete=models.CASCADE)
    product = models.CharField('Product', max_length=200)
    attribute = models.ForeignKey(Attribute, related_name='attributes', on_delete=models.CASCADE)
    isVisible = models.CharField(max_length=256, choices=[('show', 'show'), ('hide', 'hide')], default='show')

    def __str__(self):
        return str(self.product + '-' + self.attribute.name)

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
    property_description = models.CharField('Property Description', max_length=250, default='', null=False)
    format = models.CharField('Value Format', max_length=50, default='', null=False)

    class Meta:
        verbose_name_plural = "Configurations"
