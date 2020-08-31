from django.db import models
import datetime
# Create your models here.


class Transaction(models.Model):  # 创建“交易”数据表，包括收银0、储值1、入库2、出库3、加工费用4、盘亏盘盈5、外卖6、其他7的各种交易，用于每日直接成本核算
    transaction_id = models.BigIntegerField(primary_key=True)
    volume = models.FloatField(default=0.0)
    unit = models.CharField(max_length=10)
    time_date = models.DateTimeField(default=datetime.date.today())
    resource = models.IntegerField(default=0)
    category = models.CharField(max_length=10)
    explanation = models.CharField(max_length=100)