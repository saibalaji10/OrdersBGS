# Generated by Django 3.0.7 on 2020-06-28 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OrderTaker', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='orderdetails',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderdetails',
            name='product_attribute',
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_attribute',
        ),
        migrations.AlterUniqueTogether(
            name='productattribute',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='productattribute',
            name='attribute',
        ),
        migrations.RemoveField(
            model_name='productattribute',
            name='product',
        ),
        migrations.DeleteModel(
            name='Attribute',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderDetails',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='ProductAttribute',
        ),
    ]
