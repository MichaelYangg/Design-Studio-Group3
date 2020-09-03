from django.urls import path
from . import views

app_name = 'transaction'
urlpatterns = [
    path('', views.overview, name='index'),
    path('<int:transaction_id>/',views.detail,name='detail'),
    path('add/',views.add_transaction,name='add'),
    path('delete/',views.delete_transaction,name='delete'),
    path('change/',views.change_transaction,name='change')
]