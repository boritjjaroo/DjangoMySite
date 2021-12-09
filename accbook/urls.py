from django.urls import path
from . import views

app_name = 'accbook'

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', views.accounts, name='accounts'),
    path('accounts/modify/', views.accounts_modify, name='accounts_modify'),
    path('deposits/', views.deposits, name='deposits'),
    path('deposit_list/', views.deposit_list, name='deposit_list'),
    path('creditcard/', views.credit_card, name='creditcard'),
    path('fn_prod/', views.fn_prod, name='fn_prod'),
    path('fnprod_list/', views.fnprod_list, name='fnprod_list'),
    path('fn_trade/', views.fn_trade, name='fn_trade'),
    path('fntrade_list/', views.fntrade_list, name='fntrade_list'),
    path('fntrade_buy/', views.fntrade_buy, name='fntrade_buy'),
    path('monthly/', views.monthly, name='monthly'),
    path('annual/', views.annual, name='annual'),
    path('account_list/', views.account_list, name='account_list'),
    path('slip_list/', views.slip_list, name='slip_list'),
    path('slip_register/', views.slip_register, name='slip_register'),
    path('increase_order/', views.increase_order, name='increase_order'),
]