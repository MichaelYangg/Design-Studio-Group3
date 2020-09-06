from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404
from client_management.models import Member
from financials.models import Transaction

# Create your views here.

def overview(request):
    latest_register_member = Member.objects.order_by('-join_date')[:3]
    member_overview = []
    for i in range(len(latest_register_member)):
        member_overview.append({'phone': latest_register_member[i].phone, 'first_name': latest_register_member[i].first_name})
    return JsonResponse({'result':member_overview},json_dumps_params={'ensure_ascii':False})

def detail(request, phone_number):
    try:
        member = Member.objects.get(phone=phone_number)
    except Member.DoesNotExist:
        raise Http404("Member does not exist")
    else:
        member_info = {}
        member_info['phone'] = member.phone
        member_info['first_name'] = member.first_name
        member_info['last_name'] = member.last_name
        member_info['sex'] = member.gender
        member_info['nation'] = member.nation
        member_info['discount'] = member.discount
        member_info['member_points'] = member.credit
        member_info['date_joined'] = member.join_date
        member_info['address'] = member.address
        member_info['email'] = member.email
        member_info['birthday'] = member.birthday
        member_info['membership_level'] = member.member_class
        member_info['balance'] = member.balance
        return JsonResponse({'result':[member_info]},json_dumps_params={'ensure_ascii':False})

def add_member(request):
    if request.method == 'POST':
        member_info = request.POST
    else:
        member_info = request.GET
    # member_info = {'phone':'123456'}
    phone_number = member_info['phone']
    first_name = member_info['first_name']
    # 判断新增会员是否已存在
    try:
        mem = Member.objects.get(phone=phone_number)
        result = 'fail'
    except:
        Member.objects.create(phone=phone_number,first_name=first_name)
        # 第三其他的数据怎么补充
        result = 'success'
    return JsonResponse({'result':result})

def delete_member(request):
    if request.method == 'POST':
        member_info = request.POST
    else:
        member_info = request.GET
    # member_info = {'phone':'123456'}
    try:
        mem = Member.objects.get(phone=member_info['phone'])
        mem.delete()
        result = 'success'
    except:
        result = 'fail'
    return JsonResponse({'result':result})

def change_member(request):
    result = 'fail'
    member_info = request.POST
    # member_info = {'phone':'123456'}
    try:
        member = Member.objects.get(phone=member_info['phone'])
    except Member.DoesNotExist:
        raise Http404("Transaction does not exist")
    else:
        Member.objects.filter(phone=member_info['phone']).update(first_name=member_info['first_name'])
        Member.objects.filter(phone=member_info['phone']).update(last_name=member_info['last_name'])
        Member.objects.filter(phone=member_info['phone']).update(gender=member_info['sex'])
        Member.objects.filter(phone=member_info['phone']).update(nation=member_info['nation'])
        Member.objects.filter(phone=member_info['phone']).update(discount=member_info['discount'])
        Member.objects.filter(phone=member_info['phone']).update(credit=member_info['member_points'])
        Member.objects.filter(phone=member_info['phone']).update(join_date=member_info['date_joined'])
        Member.objects.filter(phone=member_info['phone']).update(address=member_info['address'])
        Member.objects.filter(phone=member_info['phone']).update(email=member_info['email'])
        Member.objects.filter(phone=member_info['phone']).update(birthday=member_info['birthday'])
        Member.objects.filter(phone=member_info['phone']).update(member_class=member_info['member_level'])
        Member.objects.filter(phone=member_info['phone']).update(balance=member_info['balance'])
        result = 'success'
    return JsonResponse({'result':result})

def deposit(request,phone_number):
    result = 'fail'
    try:
        member = Member.objects.get(phone=phone_number)
    except Member.DoesNotExist:
        raise Http404("Member does not exist")
    else:
        deposit_amount = request.POST['balance']
        # deposit_amount = 10
        original_balance = Member.objects.filter(phone=phone_number)[0]['balance']
        Member.objects.filter(phone=phone_number).update(balance=original_balance+deposit_amount)
        original_credit = Member.objects.filter(phone=phone_number)[0]['credit']
        new_credit = original_credit + deposit_amount
        Member.objects.filter(phone=phone_number).update(credit=new_credit)
        if original_credit < 1000 and new_credit >= 1000:
            Member.objects.filter(phone=phone_number).update(member_class=2)
            Member.objects.filter(phone=phone_number).update(discount=0.85)
        if original_credit < 2000 and new_credit >= 2000:
            Member.objects.filter(phone=phone_number).update(member_class=3)
            Member.objects.filter(phone=phone_number).update(discount=0.75)
        current_tran = Transaction.objects.order_by('-time_date')[0]
        current_id = current_tran.transaction_id
        new_id = current_id + 1
        Transaction.objects.create(transaction_id=new_id,volume=deposit_amount,unit='元',category='财务',resource=1,explanation='无')
        result = 'success'
    return JsonResponse({'result':result})