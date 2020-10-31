from django.db import models

# Create your models here.
class Register(models.Model):
    username = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(primary_key=True, max_length=30)
    contactno = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'register'

class Product(models.Model):
    id=models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=30, blank=True, null=True)
    dept = models.CharField(max_length=10, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    edition = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'
