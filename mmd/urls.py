from django.urls import path
from . import views

app_name = 'mmd'

urlpatterns = [
    path('', views.index, name='index'),
]