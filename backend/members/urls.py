from django.urls import path
from . import views

app_name = 'members'
urlpatterns = [
    path('', views.overview, name='index'),
    path('<int:phone_number>/',views.detail,name='detail'),
    path('deposit/<int:phone_number>/',views.deposit,name='deposit')
]