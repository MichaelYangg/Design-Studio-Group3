from django.urls import path
from . import views

app_name = 'table_payment_done'
urlpatterns = [
    path('', views.payment_confirm, name='index')
]