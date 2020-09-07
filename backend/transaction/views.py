from django.shortcuts import render
from financials.models import Transaction
from django.http import HttpResponse, JsonResponse, Http404

# Create your views here.

def overview(request):
    amount = 10
    latest_transactions = Transaction.objects.order_by('-time_date')[:amount]
    transaction_overview = []
    for tran in latest_transactions:
        transac = {'transaction_id': tran.transaction_id, 'volume': tran.volume, 'unit': tran.unit, 
            'date_time': tran.time_date, 'category': tran.category, 'resource': tran.resource, 'explanation': tran.explanation}
        transaction_overview.append(transac)
    overview = {'list':transaction_overview,'pageTotal':len(transaction_overview)}
    return JsonResponse(overview,safe=False,json_dumps_params={'ensure_ascii':False})

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
    print(request.method)
    if request.method == 'POST':
        data = request.POST
    else:
        data = request.GET
    print(data)
    assert 'list' in data
    tran_info = data['list'][0]
    # tran_info = {'transaction_id':'888888','volume':'20'}
    transaction_id = tran_info['transaction_id']
    try:
        tran = Transaction.objects.get(transaction_id=transaction_id)
        result = 'fail'
    except:
        try:
            Transaction.objects.create(transaction_id=transaction_id,volume=tran_info['volume'],
                        unit=tran_info['unit'],time_date=tran_info['time_date'],
                        resource=tran_info['resource'],category=tran_info['category'],
                        explanation=tran_info['explanation'])
            result = 'success'
        except:
            result = 'fail'
    return JsonResponse({'result':result})

def delete_transaction(request):
    transaction_id = request.POST['transaction_id']
    try:
        tran = Transaction.objects.get(transaction_id=transaction_id)
        tran.delete()
        result = 'success'
    except:
        result = 'fail'
    return JsonResponse({'result':result})

def change_transaction(request):
    tran_info = request.POST['list'][0]
    try:
        tran = Transaction.objects.get(transaction_id=tran_info['transaction_id'])
    except Transaction.DoesNotExist:
        raise Http404("Transaction does not exist")
    else:
        Transaction.objects.filter(transaction_id = tran_info['transaction_id']).update(volume=tran_info['volume'])
        Transaction.objects.filter(transaction_id = tran_info['transaction_id']).update(unit=tran_info['unit'])
        Transaction.objects.filter(transaction_id = tran_info['transaction_id']).update(time_date=tran_info['time_date'])
        Transaction.objects.filter(transaction_id = tran_info['transaction_id']).update(resource=tran_info['resource'])
        Transaction.objects.filter(transaction_id = tran_info['transaction_id']).update(category=tran_info['category'])
        Transaction.objects.filter(transaction_id = tran_info['transaction_id']).update(explanation=tran_info['explanation'])
        result = 'success'
        return JsonResponse({'result':result})