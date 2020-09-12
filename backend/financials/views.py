from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from financials.models import Transaction
import datetime
from journal.models import Daily


def daily_net_change(request):  # 目前只能手动进行直接成本核算，无法定时自动核算
    today = datetime.date.today()      # 获取当前日期
    yesterday = today-datetime.timedelta(days=1)    # 获取昨天日期
    category_list = ['财务','白条净膛鹅','白条湖鸭','肉鸡','鸡胸','五花肉（瘦）','纯瘦肉','纯排骨','羊排骨','牛柳（里脊）','梭子蟹','花蛤','扇贝（地播）','多宝鱼','桂鱼','活白虾','白萝卜','藕','黄瓜','荔浦芋头','胡萝卜','绿菜花','彩椒','柿子椒','空心菜','芥兰','番茄','茄子','韭菜','土豆','好面缘面粉25kg','泰国糯米','东北大米','莜麦面','散鸡蛋','花生米','茅台','红星二锅头','青岛啤酒','可口可乐','雪碧','北冰洋','加多宝','美汁源 橙汁']
    Daily.objects.filter(date=today).delete()

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

        Daily.objects.create(id=Daily.objects.all().count()+1, account_type=category,       # 新id为行数
                                 net_profit=today_total_volume, unit=unit, date=today, balance=balance)

    return HttpResponse('result: success')
