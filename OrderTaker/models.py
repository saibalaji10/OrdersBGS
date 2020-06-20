from django.db import models


class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=200)
    item_type = models.CharField(max_length=200)

    def __int__(self): # __unicode__ on Python 2
        return self.item_id


    def getItemType(self):
        return self.item_type


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __int__(self):  # __unicode__ on Python 2
        return self.order_id

    def getItems(self):
        return self.item_id

