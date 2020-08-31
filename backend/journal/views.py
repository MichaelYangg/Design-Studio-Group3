from django.shortcuts import render, redirect
from django.urls import path
from django.db.models import Sum

# Create your views here.
from django.http import HttpResponse
from journal.models import Daily, Monthly
from .forms import DailyFrom, MonthlyFrom
from . import views

# Daily Journal에 대한 View
def daily(request):
    data = Daily.objects.all()
    # 정보 제출(Submit) 시, Daily(account_type, net_profit, unit, date, balance)의 데이터베이스 저장
    if request.method == 'POST':
        form = DailyFrom(request.POST)
        if form.is_valid():
            check = form['account_type'].value()
            unit = form['unit'].value()
            date = form['date'].value()
            net_profit = (float)(form['net_profit'].value())
            # Balance 계산(Profit Balance와 Loss Balance를 따로 구해서, 두 값의 '차이(-)'를 구하면 이전 값까지의 balance를 구함)
            if(data.count() < 1):
                balance = 0.0
            else:
                balance_pTotal = Daily.objects.filter(account_type='P').aggregate(Sum('net_profit'))['net_profit__sum']
                balance_mTotal = Daily.objects.filter(account_type='L').aggregate(Sum('net_profit'))['net_profit__sum']
                if(balance_pTotal == None):
                    balance_pTotal = 0
                elif(balance_mTotal == None):
                    balance_mTotal = 0
                balance = balance_pTotal - balance_mTotal
            # Account Type가 'profit(P)' or 'loss(L)'에 따라 DB에 구분 저장
            if(check == 'P'):
                Daily(account_type = check, net_profit = net_profit, unit = unit, date = date, balance = balance + net_profit).save()
            elif(check == 'L'):
                Daily(account_type = check, net_profit = net_profit, unit = unit, date = date, balance = balance - net_profit).save()
            else:
                EOFError
        return redirect('/daily')
    else:
        form = DailyFrom()
    
    return render(request, 'daily.html', {'dailyData': data, 'form': form})

# Monthly Journal에 대한 View
def monthly(request):
    data = Monthly.objects.all()
    # 정보 제출(Submit) 시, Monthly(month, revenue, cost, net_profit, balance, date, recorder)의 데이터베이스 저장
    if request.method == 'POST':
        form = MonthlyFrom(request.POST)
        if form.is_valid():
            date = form['date'].value()
            revenue = (float)(form['revenue'].value())
            cost = (float)(form['cost'].value())
            net_profit = revenue - cost
            # Balance 계산
            if(data.count() < 1):
                balance = 0.0
            else:
                balance = Monthly.objects.aggregate(Sum('net_profit'))['net_profit__sum']
                balance = (float)(balance)
            Monthly(net_profit = net_profit, month = date, balance = balance + net_profit, date = date, revenue = revenue, cost = cost, recorder = "1").save()
    else:
        form = MonthlyFrom()
    return render(request, 'monthly.html', {'monthlyData':data, 'form':form})

# Monthly Analysis에 대한 View
def profitAndLoss(request):
    # html에서 사용할 수 있는 데이터 생성 및 초기화
    data = list(range(12))
    for i in range(12):
        data[i] = {'month' : i + 1, 'revenue' : 0, 'cost' : 0, 'net_profit': 0, 'balance': 0, 'result': 'none'}
    # Monthly에 있는 데이터베이스 사용
    monthlyData  = Monthly.objects
    dateData = monthlyData.values('date__month') 
    # 각 월에 대한 revenue, cost, net_profit에 대하서 종합 계산
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
