from django.urls import path
from . import views

app_name = 'realestate'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:listitem_id>/', views.detail, name='detail'),
    path('item/modify/<int:listitem_id>/', views.item_modify, name='item_modify'),
    path('naver/', views.naver, name='naver'),
    path('check/', views.check, name='check'),
    path('favorite/', views.favorite, name='favorite'),
    path('multi/', views.multi, name='multi'),
]