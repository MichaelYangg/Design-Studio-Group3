from django.urls import path
from . import views

app_name = 'members'
urlpatterns = [
    path('', views.overview, name='index'),
    path('<int:phone_number>/',views.detail,name='detail'),
    path('deposit/<int:phone_number>/',views.deposit,name='deposit'),
    path('add_member/',views.add_member,name='add'),
    path('delete_member/',views.delete_member,name='delete'),
    path('change_member/',views.change_member,name='change')
]