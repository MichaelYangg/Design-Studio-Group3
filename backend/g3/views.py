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