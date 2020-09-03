from django.shortcuts import render
from financials.models import Transaction
from django.http import HttpResponse, JsonResponse, Http404

# Create your views here.

def overview(request):
    latest_transactions = Transaction.objects.order_by('-time_date')[:3]
    transaction_overview = {}
    for i in range(len(latest_transactions)):
        transaction_overview[i] = {
            'transaction_id': latest_transactions[i].transaction_id, 'Volume': latest_transactions[i].volume,
            'Unit': latest_transactions[i].unit, 'date_time': latest_transactions[i].time_date, 
            'Category': latest_transactions[i].category}
    return JsonResponse(transaction_overview,safe=False,json_dumps_params={'ensure_ascii':False})

def detail(request, transaction_id):
    try:
        tran = Transaction.objects.get(transaction_id=transaction_id)
    except Transaction.DoesNotExist:
        raise Http404("Transaction does not exist")
    else:
        tran_info = {}
        tran_info['transaction_id'] = tran.transaction_id
        tran_info['Volume'] = tran.volume
        tran_info['Unit'] = tran.unit
        tran_info['date_time'] = tran.time_date
        tran_info['Resource'] = tran.resource
        tran_info['Category'] = tran.category
        tran_info['Explanation'] = tran.explanation
        return JsonResponse(tran_info,safe=False,json_dumps_params={'ensure_ascii':False})

def add_transaction(request):
    # tran_info = request.GET
    tran_info = {'transaction_id':'888888','volume':'20'}
    transaction_id = tran_info['transaction_id']
    try:
        tran = Transaction.objects.get(transaction_id=transaction_id)
        result = 'fail'
    except:
        try:
            Transaction.objects.create(transaction_id=transaction_id,volume=tran_info['volume'])
            result = 'success'
        except:
            result = 'fail'
    return JsonResponse({'result':result})