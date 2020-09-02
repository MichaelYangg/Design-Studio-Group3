from django.shortcuts import render
from django.http import HttpResponse
from client_management.models import discount_policy
from client_management.models import Member
from django.core import serializers
import datetime
import xmltodict
import json


def discount(request):
    data = discount_policy.objects.all()                           # discount_policy是存储优惠信息的数据表
    length = data.count()                                          # 获取表数据总长度
    result = discount_policy.objects.filter(policy_id=length - 1)  # 取出最后一行（即最新）数据
    result_start = result.values('start_date')[0]['start_date']    # 取出这行数据的开始日期
    result_end = result.values('end_date')[0]['end_date']          # 取出这行数据的截止日期
    today = datetime.date.today()
    policy = result.values('policy_content')[0]

    resultxml = xmltodict.unparse(policy, pretty=True)

    if result_start < today and result_end > today:                # 若今日日期在这行数据有效期内，返回该优惠策略的内容
        return HttpResponse(resultxml)
    else:
        return HttpResponse(None)


def add_credit(request):  # 会员消费增加积分
    consumption = 100     # 此数值目前仅用于测试，日后需要修改，应为计算出的用户应付的价格
    phone = 12345678900   # 此数值目前仅用于测试，日后需要修改，应为用户电话号码
    try:
        target = Member.objects.filter(phone=phone)
        original_credit = target.values('credit')[0]['credit']
        new_credit = original_credit + consumption
        Member.objects.filter(phone=phone).update(credit=new_credit)
        if original_credit < 1000 and new_credit >= 1000:
            Member.objects.filter(phone=phone).update(member_class=2)
            Member.objects.filter(phone=phone).update(discount=0.85)
        if original_credit < 2000 and new_credit >= 2000:
            Member.objects.filter(phone=phone).update(member_class=3)
            Member.objects.filter(phone=phone).update(discount=0.75)
        resultsuccess = json.dumps({'result': 'success'})
        return HttpResponse(resultsuccess)

    except Exception:
        resultfail = json.dumps({'result': 'fail'})
        return HttpResponse(resultfail)
