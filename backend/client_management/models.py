from django.db import models
import datetime
# Create your models here.


class discount_policy(models.Model):
    policy_id = models.AutoField(primary_key=True)
    policy_content = models.CharField(max_length=500)
    start_date = models.DateField(default=datetime.date.today())
    person_in_charge = models.BigIntegerField(default=10000000)
    end_date = models.DateField(default=datetime.date.today())


class Member(models.Model):
    phone = models.BigIntegerField(primary_key=True)
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=30)
    gender = models.BooleanField(default=0)
    nation = models.CharField(max_length=20)
    join_date = models.DateField(default=datetime.date.today())
    credit = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    address = models.CharField(max_length=50)
    member_class = models.IntegerField(default=1)
    email = models.CharField(max_length=30)
    birthday = models.DateField(default='2001-01-01')
    discount = models.FloatField(default=1.0)