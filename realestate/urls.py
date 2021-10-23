from django.urls import path
from .views import base_views, address_views, price_views, jibun_views

app_name = 'realestate'

urlpatterns = [
    path('', base_views.index, name='index'),
    path('<int:listitem_id>/', base_views.detail, name='detail'),
    path('json/<int:article_no>/', base_views.json_view, name='json_view'),
    path('item/modify/<int:listitem_id>/', base_views.item_modify, name='item_modify'),
    path('alllist/', base_views.alllist, name='alllist'),
    path('declared/get', base_views.declared_get, name='declared_get'),
    path('declared/update', base_views.declared_update, name='declared_update'),
    path('naver/', base_views.naver, name='naver'),
    path('naver/register/', base_views.naver_register, name='naver_register'),
    path('naver/register/action/', base_views.naver_register_action, name='naver_register_action'),
    path('naver/link/', base_views.naver_link, name='naver_link'),
    path('check/', base_views.check, name='check'),
    path('arch_owner/', base_views.arch_owner, name='arch_owner'),
    path('price/', price_views.price, name='price'),
    path('price/search/', price_views.price_search, name='price_search'),
    path('address/', address_views.address, name='address'),
    path('address/load/', address_views.address_load, name='address_load'),
    path('address/upload/', address_views.address_upload, name='address_upload'),

    path('jibun/list/', jibun_views.jibun_list, name='jibun_list'),
]