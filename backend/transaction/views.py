from django.shortcuts import render
from financials.models import Transaction
from django.http import HttpResponse, JsonResponse, Http404

# Create your views here.

def overview(request):
    latest_transactions = Transaction.objects.order_by('-time_date')[:3]
    transaction_overview = {}
    for i in range(len(latest_transactions)):
        transaction_overview[i] = {
            'transaction_id': latest_transactions[i].transaction_id, 'volume': latest_transactions[i].volume,
            'unit': latest_transactions[i].unit, 'date_time': latest_transactions[i].time_date, 
            'category': latest_transactions[i].category, 'resource': latest_transactions[i].resource,
            'explanation': latest_transactions[i].explanation}
    return JsonResponse(transaction_overview,safe=False,json_dumps_params={'ensure_ascii':False})

def detail(request, transaction_id):
    try:
        tran = Transaction.objects.get(transaction_id=transaction_id)
    except Transaction.DoesNotExist:
        raise Http404("Transaction does not exist")
    else:
        tran_info = {}
        tran_info['transaction_id'] = tran.transaction_id
        tran_info['volume'] = tran.volume
        tran_info['unit'] = tran.unit
        tran_info['date_time'] = tran.time_date
        tran_info['resource'] = tran.resource
        tran_info['category'] = tran.category
        tran_info['explanation'] = tran.explanation
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