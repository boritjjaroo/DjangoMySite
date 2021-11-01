from django.urls import path
from . import views

app_name = 'accbook'

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', views.accounts, name='accounts'),
    path('accounts/modify/', views.accounts_modify, name='accounts_modify'),
    path('deposits/', views.deposits, name='deposits'),
    path('creditcard/', views.credit_card, name='creditcard'),
]