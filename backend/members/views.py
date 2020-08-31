from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404
from client_management.models import Member

# Create your views here.

def overview(request):
    latest_register_member = Member.objects.order_by('-join_date')[:3]
    member_overview = {}
    for i in range(len(latest_register_member)):
        member_overview[i] = {'Phone Number': latest_register_member[i].phone, 'Deposit': latest_register_member[i].balance}
    return JsonResponse(member_overview)

def detail(request, phone_number):
    try:
        member = Member.objects.get(phone=phone_number)
    except Member.DoesNotExist:
        raise Http404("Member does not exist")
    else:
        member_info = {}
        member_info['Phone Number'] = member.phone
        member_info['First Name'] = member.first_name
        member_info['Last Name'] = member.last_name
        member_info['Gender'] = member.gender
        member_info['Nation'] = member.nation
        member_info['Discount'] = member.discount
        member_info['Credit'] = member.credit
        member_info['Join Date'] = member.join_date
        member_info['Address'] = member.address
        member_info['Email'] = member.email
        member_info['Birthday'] = member.birthday
        member_info['Level'] = member.member_class
        return JsonResponse(member_info)

def add_member(request):
    # member_info = request.GET
    member_info = {'name': 'yang', 'phone':'123456'}
    first_name = member_info['name']
    phone_number = member_info['phone']
    # 判断新增会员是否已存在
    try:
        mem = Member.objects.get(phone=phone_number)
        result = 'fail'
    except:
        Member.objects.create(phone=phone_number,first_name=first_name)
        # 这里有一些问题，首先前端传回的手机号最好应该是BigInt的格式
        # 第二名字需要确认last name/first name
        # 第三其他的数据怎么补充
        result = 'success'
    return JsonResponse({'result':result})

def delete_member(request):
    # member_info = request.GET
    member_info = {'phone':'123456'}
    try:
        mem = Member.objects.get(phone=member_info['phone'])
        mem.delete()
        # 这里不需要姓名
        result = 'success'
    except:
        result = 'fail'
    return JsonResponse({'result':result})

def change_member(request):
    # member_info = request.GET
    member_info = {'phone':'123456'}
    try:
        member = Member.objects.get(phone=member_info['phone'])
        result = 'success'
    except:
        result = 'fail'
    return JsonResponse({'result':result})

def deposit(request,phone_number):
    try:
        member = Member.objects.get(phone=phone_number)
    except Member.DoesNotExist:
        raise Http404("Member does not exist")
    else:
        # deposit_amount = request.GET['balance'] # 待和前端确认修改
        deposit_amount = 10
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
        result = 'success'
        return JsonResponse({'result':result})