from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
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

def deposit(request,phone_number):
    try:
        member = Member.objects.get(phone=phone_number)
    except Member.DoesNotExist:
        raise Http404("Member does not exist")
    else:
        # deposit_amount = request.GET['deposit'] # 待和前端确认修改
        deposit_amount = 10
        member.balance += deposit_amount
        member.credit += deposit_amount
        result = 'success'
        return JsonResponse({'result':result})