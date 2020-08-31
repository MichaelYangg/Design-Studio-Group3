"""group3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from journal.views import daily, monthly, profitAndLoss     #Journal.Views의 function 호출
from django.urls import path, include
from client_management.views import discount  # 虽然报错，但能成功导入
from client_management.views import add_credit
from financials.views import daily_net_change

urlpatterns = [
    path('discount_policy/', discount),         # 回给G1的优惠信息网址
    path('daily_net_change', daily_net_change),  # 今日日结净变化查询
    path('add_credit/', add_credit),            # 消费增加积分
    path('daily/', daily),                      # Daily Journal page  
    path('monthly/', monthly),                  # Monthly Journal page
    path('monthly_analysis/', profitAndLoss),   # Monthly Profit & Loss analysis page
    path('admin/', admin.site.urls),
    path('members/', include('members.urls')), # 增删查改会员信息
    path('table_payment_done/',include('table_payment_done.urls')) # 回给1组交易确认
]
