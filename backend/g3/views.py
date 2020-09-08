from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from client_management.models import Member
from financials.models import Transaction
import xmltodict

# Create your views here.

def other_cost(request):
    xmlinfo = request.POST
    data = xmltodict.parse(xmlinfo)
    cost = data['cost']
    current_tran = Transaction.objects.order_by('-transaction_id')[0]
    current_id = current_tran.transaction_id
    new_id = current_id + 1
    try:
        Transaction.objects.create(transaction_id=new_id,volume=cost,unit='元',resource=4,category='财务',explanation='无')
        result = 'success'
    except:
        result = 'fail'
    return JsonResponse({'result':'success'})


def payment_done_add_credit(request):
    # payment = request.POST
    payment = {'payment_method': 'cash', 'discount_price': 100, 'time': '2020-09-04 19:00:00', 'telephone': 12345678900}  # 此数值仅用于测试，具体看G1的字段名
    volume = payment['discount_price']
    phone = payment['telephone']
    # 消费增加积分
    try:
        target = Member.objects.filter(phone=phone)
    finally:
        original_credit = target.values('credit')[0]['credit']
        new_credit = original_credit + volume
        Member.objects.filter(phone=phone).update(credit=new_credit)
        if original_credit < 1000 and new_credit >= 1000:
            Member.objects.filter(phone=phone).update(member_class=2)
            Member.objects.filter(phone=phone).update(discount=0.85)
        if original_credit < 2000 and new_credit >= 2000:
            Member.objects.filter(phone=phone).update(member_class=3)
            Member.objects.filter(phone=phone).update(discount=0.75)
    # 记账
    time = payment['time']
    current_tran = Transaction.objects.order_by('-transaction_id')[0]
    current_id = current_tran.transaction_id
    new_id = current_id + 1
    try:
        Transaction.objects.create(transaction_id=new_id,volume=volume,unit='元',resource=0,category='财务',explanation='无',time_date=time)
        payment_status = 0
    except:
        payment_status = 1
    return JsonResponse({'payment_status': payment_status})

def stock_in(request):
    xmlinfo = request.POST
    data = xmltodict.parse(xmlinfo)
    current_tran = Transaction.objects.order_by('-transaction_id')[0]
    current_id = current_tran.transaction_id
    new_id = current_id + 1
    try:
        Transaction.objects.create(transaction_id=new_id,volume=data['amount'],unit=data['unit'],resource=2,category=data['mName'],explanation='无')
        cost = float(data['price']) * float(data['amount'])
        Transaction.objects.create(transaction_id=new_id+1,volume=-cost,unit='元',resource=2,category='财务',explanation='无')
        result = 'success'
    except:
        result = 'fail'
    return JsonResponse({'result':result})

def stock_out(request):
    xmlinfo = request.POST
    data = xmltodict.parse(xmlinfo)
    data = data['raw_material']
    result = 'success'
    for info in data:
        current_tran = Transaction.objects.order_by('-transaction_id')[0]
        current_id = current_tran.transaction_id
        new_id = current_id + 1
        volume = float(info['amount'])
        unit = info['unit']
        category = info['mName']
        try:
            Transaction.objects.create(transaction_id=new_id,volume=-volume,unit=unit,resource=3,category=category,explanation='无')
        except:
            result = 'fail'
    return JsonResponse({'result':result})

def inventory(request):
    xmlinfo = request.POST
    data = xmltodict.parse(xmlinfo)
    result = 'success'
    for info in data:
        current_tran = Transaction.objects.order_by('-transaction_id')[0]
        current_id = current_tran.transaction_id
        new_id = current_id + 1
        volume = float(info['stock'])
        category = info['mName']
        unit = info['unit']
        try:
            Transaction.objects.create(transaction_id=new_id,volume=-volume,unit=unit,resource=5,category=category,explanation='无')
        except:
            result = 'fail'
    return JsonResponse({'result':result})
