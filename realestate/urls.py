from django.urls import path
from . import views

app_name = 'realestate'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:listitem_id>/', views.detail, name='detail'),
    path('json/<int:article_no>/', views.json_view, name='json_view'),
    path('item/modify/<int:listitem_id>/', views.item_modify, name='item_modify'),
    path('alllist/', views.alllist, name='alllist'),
    path('declared/get', views.declared_get, name='declared_get'),
    path('declared/update', views.declared_update, name='declared_update'),
    path('naver/', views.naver, name='naver'),
    path('naver/register/', views.naver_register, name='naver_register'),
    path('naver/register/action', views.naver_register_action, name='naver_register_action'),
    path('naver/link/', views.naver_link, name='naver_link'),
    path('check/', views.check, name='check'),
    path('price/', views.price, name='price'),
]