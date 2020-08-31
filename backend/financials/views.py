from django.shortcuts import render
from django.http import HttpResponse
from financials.models import transaction
import datetime


def direct_cost_calculation(request):  # 目前只能手动进行直接成本核算，无法定时自动核算
    today = datetime.date.today()      # 获取当前日期
    today_cost = transaction.objects.filter(time_date__startswith=today, unit='元', volume__lt=0).values('volume')
    # 取出今天发生的，单位为元，数量为负数的交易（单位为元的交易即金钱交易，货物交易则不包含在内；数量为负数则代表是成本）
    # today_cost的数据类型为i个字典，i = 今天发生的金钱交易次数

    today_total = 0                    # 初始化今日直接成本总和，为0
    for i in range(len(today_cost)):   # 对今天的所有成本数据进行累加
        today_total = today_total + today_cost[i]['volume']
    today_total = 0 - today_total      # 成本应使用正数显示，故取相反数
    return HttpResponse('今日直接成本：' + str(today_total) + '元')   # 返回今日直接成本总和
