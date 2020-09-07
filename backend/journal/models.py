from django.db import models

# Create your models here.
class Daily(models.Model):
    ACCOUNT_CHOICE = (
        ('P', 'Profit'),
        ('L', 'Loss'),
    )
    account_type = models.CharField(max_length=10, choices=ACCOUNT_CHOICE) 
    net_profit = models.FloatField()
    unit = models.CharField(max_length=50) #yuan
    date = models.DateField(auto_now=False, auto_now_add=False)
    balance = models.FloatField()

class Monthly(models.Model):
    month = models.DateField(auto_now=False, auto_now_add=False)
    revenue = models.DecimalField(max_digits=8, decimal_places=2)
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    net_profit = models.DecimalField(max_digits=8, decimal_places=2)
    balance = models.FloatField()
    date = models.DateField(auto_now=False, auto_now_add=False)
    recorder = models.BigIntegerField()

