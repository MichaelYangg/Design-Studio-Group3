from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from client_management.models import Member
from financials.models import Transaction

# Create your views here.

def other_cost(request):
    cost = request.POST
    current_id = Transaction.objects.order_by('-transaction_id')[:3]
    