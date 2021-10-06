from django.urls import path
from . import views

app_name = 'realestate'

urlpatterns = [
    path('', views.index2, name='index2'),
    path('<int:listitem_id>/', views.detail2, name='detail2'),
    path('json/<int:article_no>/', views.json_view, name='json_view'),
    path('item/modify/<int:listitem_id>/', views.item_modify2, name='item_modify2'),
    path('naver/', views.naver, name='naver'),
    path('check/', views.check, name='check'),
    path('favorite/', views.favorite, name='favorite'),
    path('multi/', views.multi, name='multi'),
    path('price/', views.price, name='price'),
]