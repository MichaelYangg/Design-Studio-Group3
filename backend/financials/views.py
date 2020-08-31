from django.shortcuts import render
from django.http import HttpResponse
from financials.models import Transaction
import datetime
import json


def daily_net_change(request):  # 目前只能手动进行直接成本核算，无法定时自动核算
    today = datetime.date.today()      # 获取当前日期
<<<<<<< HEAD
    today_cost = Transaction.objects.filter(time_date__startswith=today, unit='元', volume__lt=0).values('volume')
    # 取出今天发生的，单位为元，数量为负数的交易（单位为元的交易即金钱交易，货物交易则不包含在内；数量为负数则代表是成本）
    # today_cost的数据类型为i个字典，i = 今天发生的金钱交易次数
=======
    category_list = transaction.objects.values('category').distinct()
    # 提取出无重复值的列表，为transaction表中各种不同的category（财务、白菜、猪肉等，今日有多少种不同的transaction就包含多少个）
    # category_list的数据类型为i个字典，i = 不同的category数量
>>>>>>> e7d975baff82d6219ad9f72b40f93ab00042fd2a

    today_net_change = {}
    for category_dict in category_list:
        category = category_dict['category']
        unit = transaction.objects.filter(category=category).values('unit')[0]['unit']  # 在数据库中查出这一category的数据使用的unit，用于显示
        today_category_volume = transaction.objects.filter(time_date__startswith=today, category=category).values('volume')
        # 取出今天发生的，某特定category的交易
        # today_category_volume的数据类型为i个字典，i = 今天发生的该category交易次数

        today_total_volume = 0                        # 初始化今日该类交易总数量，为0
        for i in range(len(today_category_volume)):   # 对今天中这一category的所有数量数据进行累加
            today_total_volume = today_total_volume + today_category_volume[i]['volume']

        if today_total_volume > 0:
            today_net_change[category] = '+' + str(today_total_volume) + unit   # 在字典中加入此category及对应数据
        else:
            today_net_change[category] = str(today_total_volume) + unit         # 在字典中加入此category及对应数据

    today_net_change_json = json.dumps(today_net_change, ensure_ascii=False)    # 字典数据类型转化为json数据类型，并确保汉字正常显示

    return HttpResponse(today_net_change_json)                                  # 返回今日各类category的净出入量
