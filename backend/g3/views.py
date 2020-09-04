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
    current_tran = Transaction.objects.order_by('-time_date')[0]
    current_id = current_tran.transaction_id
    new_id = current_id + 1
    try:
        Transaction.objects.create(transaction_id=new_id,volume=cost,unit='元',resource=4,category='财务',explanation='无')
        result = 'success'
    except:
        result = 'fail'
    return JsonResponse({'result':'success'})


def payment_done_add_credit(request):
    # add_credit_info = request.GET
    payment = {'method': 'cash', 'discount_price': 100, 'time': '2020-09-04 19:00:00', 'phone': 12345678900}  # 此数值仅用于测试，具体看G1的字段名
    volume = payment['discount_price']
    phone = payment['phone']

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


    return JsonResponse({'result':'success'})