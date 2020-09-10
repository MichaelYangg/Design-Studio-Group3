from django.urls import path
from . import views

app_name = 'g3'
urlpatterns = [
    path('order_other_cost', views.other_cost, name='other_cost'),
    path('confirm_payment/', views.payment_done_add_credit, name='payment'),
    path('stock_in/',views.stock_in,name='stock_in'),
    path('stock_out/',views.stock_out,name='stock_out'),
    path('inventory/',views.inventory,name='inventory')
]