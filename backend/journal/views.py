import json
from django.shortcuts import render, redirect
from django.urls import path
from django.db.models import Sum

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from journal.models import Daily, Monthly
from .forms import DailyFrom, MonthlyFrom
from . import views
import datetime

# # Daily Journal的 View
# def daily(request):
#     data = Daily.objects.all()
#     # 输入信息后(Submit) , Daily(account_type, net_profit, unit, date, balance)储存在数据库里
#     if request.method == 'POST':
#         form = DailyFrom(request.POST)
#         if form.is_valid():
#             check = form['account_type'].value()
#             unit = form['unit'].value()
#             date = form['date'].value()
#             net_profit = (float)(form['net_profit'].value())
#             # Balance 计算(分别计算Profit Balance和 Loss Balance, 计算两者之差(-)，并计算最更新的balance)
#             if(data.count() < 1):
#                 balance = 0.0
#             else:
#                 balance_pTotal = Daily.objects.filter(account_type='P').aggregate(Sum('net_profit'))['net_profit__sum']
#                 balance_mTotal = Daily.objects.filter(account_type='L').aggregate(Sum('net_profit'))['net_profit__sum']
#                 if(balance_pTotal == None):
#                     balance_pTotal = 0
#                 elif(balance_mTotal == None):
#                     balance_mTotal = 0
#                 balance = balance_pTotal - balance_mTotal
#             # Account Type根据 'profit(P)' or 'loss(L)'分别储存在DB
#             if(check == 'P'):
#                 Daily(account_type = check, net_profit = net_profit, unit = unit, date = date, balance = balance + net_profit).save()
#             elif(check == 'L'):
#                 Daily(account_type = check, net_profit = net_profit, unit = unit, date = date, balance = balance - net_profit).save()
#             else:
#                 EOFError
#         return redirect('/daily')
#     else:
#         form = DailyFrom()
    
#     return render(request, 'daily.html', {'dailyData': data, 'form': form})

# yzy
def daily(request):
    account = Daily.objects.order_by('-date')
    # Daily.objects.create(account_type='白菜',net_profit='30',unit='吨',balance='20',date=datetime.datetime.today())
    print(account)
    account_overview = [{'account_type':acc.account_type,'net_profit':acc.net_profit,'unit':acc.unit,'date':acc.date,'balance':acc.balance} for acc in account]
    return JsonResponse({'list':account_overview,'pageTotal':len(account_overview)},safe=False,json_dumps_params={'ensure_ascii':False})

# Monthly Journal的 View
def monthly(request):
    data = Monthly.objects.all()
    # 输入信息后(Submit) , Monthly(month, revenue, cost, net_profit, balance, date, recorder)储存在DB
    if request.method == 'POST':
        form = MonthlyFrom(request.POST)
        if form.is_valid():
            date = form['date'].value()
            revenue = (float)(form['revenue'].value())
            cost = (float)(form['cost'].value())
            net_profit = revenue - cost
            # Balance 计算
            if(data.count() < 1):
                balance = 0.0
            else:
                balance = Monthly.objects.aggregate(Sum('net_profit'))['net_profit__sum']
                balance = (float)(balance)
            Monthly(net_profit = net_profit, month = date, balance = balance + net_profit, date = date, revenue = revenue, cost = cost, recorder = "1").save()
    else:
        form = MonthlyFrom()
    return render(request, 'monthly.html', {'monthlyData':data, 'form':form})


# Monthly Analysis的 View
def profitAndLoss(request):
    #生成并初始化能在 html使用的数据
    data = list(range(12))
    for i in range(12):
        data[i] = {'month' : i + 1, 'revenue' : 0, 'cost' : 0, 'net_profit': 0, 'balance': 0, 'result': 'none'}
    # Monthly에 있는 데이터베이스 사용
    monthlyData  = Monthly.objects
    dateData = monthlyData.values('date__month') 
    # 对各月 revenue, cost, net_profit进行综合计算
    for i in range(dateData.count()):
        month = dateData[i]['date__month']
        for j in range(12):
            if(month == j):
                data[j]['revenue'] = data[j]['revenue'] + (monthlyData.values('revenue'))[i]['revenue']
                data[j]['cost']  = data[j]['cost'] + (monthlyData.values('cost'))[i]['cost']
                data[j]['net_profit'] = data[j]['net_profit'] + ((monthlyData.values('revenue'))[i]['revenue'] - (monthlyData.values('cost'))[i]['cost'])
    # 计算各月 Balance, 判断'profit' or 'loss'
    for i in range(12):
        if(i == 0):
            data[i]['balance'] = data[i]['net_profit']
        else:
            for j in range(i):
                data[i]['balance'] = data[i]['balance'] + data[j]['balance']
            data[i]['balance'] = data[i]['balance'] + data[i]['net_profit']
        if(data[i]['balance'] > 0):
            data[i]['result'] = 'profit'
        elif(data[i]['balance'] < 0):
            data[i]['result'] = 'loss'
        else:
            data[i]['result'] = 'none'
    return render(request, 'profitAndLoss.html', {'data': data})
