from django.db import models

# Create your models here.



class Sale(models.Model):
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)