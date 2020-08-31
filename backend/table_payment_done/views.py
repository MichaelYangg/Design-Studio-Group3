from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.


# 接受支付方式，返回结果
def payment_confirm(request):
    payment_status = 0
    return JsonResponse({'payment_status': payment_status})

