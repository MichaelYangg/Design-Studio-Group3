from django.db import models
import datetime

# Create your models here.
class Daily(models.Model):
    ACCOUNT_CHOICE = (
        ('财务','财务'),
        ('白菜','白菜'),
        ('猪肉','猪肉'),
        ('生菜','生菜'),
        ('菜心','菜心'),
        ('羊肉','羊肉'),
        ('牛肉','牛肉'),
        ('醋','醋'),
        ('白糖','白糖'),
        ('盐','盐'),
        ('大米','大米'),
        ('小米','小米'),
        ('糯米','糯米'),
        ('调和油','调和油'),
        ('菜油','菜油'),
        ('酱油','酱油'),
        ('面粉','面粉'),
        ('米粉','米粉'),
        ('挂面','挂面'),
        ('黄豆','黄豆'),
        ('香菇','香菇'),
        ('海带','海带'),
    )
    account_type = models.CharField(max_length=10, choices=ACCOUNT_CHOICE) 
    net_profit = models.FloatField()
    unit = models.CharField(max_length=50) 
    date = models.DateField(auto_now=False, auto_now_add=False)
    balance = models.FloatField()

class Monthly(models.Model):
    month = models.DateField(auto_now=False, auto_now_add=False)
    revenue = models.DecimalField(max_digits=8, decimal_places=2)
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    net_profit = models.DecimalField(max_digits=8, decimal_places=2)
    balance = models.FloatField()
    date = models.DateField(auto_now=False, auto_now_add=False,default=datetime.datetime.today())
    recorder = models.BigIntegerField()

