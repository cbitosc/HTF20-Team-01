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
