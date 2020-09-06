from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from financials.models import Transaction
import datetime
from journal.models import Daily


def daily_net_change(request):  # 读daily，读transaction，写daily
    today = datetime.date.today()                   # 获取当前日期
    yesterday = today-datetime.timedelta(days=1)    # 获取昨天日期
#    category_list = ['财务','白菜','猪肉','生菜','菜心','羊肉','牛肉','醋','白糖',
#                     '盐','大米','小米','糯米','调和油','菜油','酱油','面粉','米粉','挂面','黄豆','香菇','海带']  # 之后再用这个list
    category_list = ['财务', '白菜', '猪肉', '羊肉', '盐', '牛肉']

    for category in category_list:
        old_balance = Daily.objects.filter(account_type=category, date=yesterday).values('balance')[0]['balance']
        unit = Daily.objects.filter(account_type=category).values('unit')[0]['unit']  # 在数据库中查出这一category的数据使用的unit，用于显示
        try:
            today_category_volume = Transaction.objects.filter(time_date__startswith=today, category=category).values('volume')
            # 取出今天发生的，某特定category的交易
            # today_category_volume的数据类型为i个字典，i = 今天发生的该category交易次数

            today_total_volume = 0                        # 初始化今日该类交易总数量，为0
            for i in range(len(today_category_volume)):   # 对今天中这一category的所有数量数据进行累加
                today_total_volume = today_total_volume + today_category_volume[i]['volume']
            balance = old_balance + today_total_volume

        except:
            today_total_volume = 0

        Daily.objects.create(id=Daily.objects.all().count()+2, account_type=category,       # 新id为行数+2
                                 net_profit=today_total_volume, unit=unit, date=today, balance=balance)

    return HttpResponse('result:success')
