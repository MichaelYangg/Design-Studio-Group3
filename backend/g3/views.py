from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from client_management.models import Member
from financials.models import Transaction

# Create your views here.

def other_cost(request):
    cost = request.POST
    current_tran = Transaction.objects.order_by('-time_date')[0]
    current_id = current_tran.transaction_id
    new_id = current_id + 1