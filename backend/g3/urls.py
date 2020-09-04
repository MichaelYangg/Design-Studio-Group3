from django.urls import path
from . import views

app_name = 'g3'
urlpatterns = [
    path('order_other_cost/', views.other_cost, name='other_cost'),
    path('table_payment_done/', views.payment_done_add_credit, name='payment')
]