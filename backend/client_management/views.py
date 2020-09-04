from django.shortcuts import render
from django.http import HttpResponse
from client_management.models import DiscountPolicy
from client_management.models import Member
from django.core import serializers
import datetime
import xmltodict
import json


def discount(request):
    data = DiscountPolicy.objects.all()                           
    length = data.count()                                          # 获取表数据总长度
    result = DiscountPolicy.objects.filter(policy_id=length - 1)   # 取出最后一行（即最新）数据
    result_start = result.values('start_date')[0]['start_date']    # 取出这行数据的开始日期
    result_end = result.values('end_date')[0]['end_date']          # 取出这行数据的截止日期
    today = datetime.date.today()
    policy = result.values('policy_content')[0]

    resultxml = xmltodict.unparse(policy, pretty=True)

    if result_start < today and result_end > today:                # 若今日日期在这行数据有效期内，返回该优惠策略的内容
        return HttpResponse(resultxml)
    else:
        return HttpResponse(None)



