from django.shortcuts import render
from django.http import HttpResponse
from .models import MMDList


def index(request):
    result_list = MMDList.objects.order_by('character')

    context = { 'list': result_list }
    return render(request, 'mmd/list.html', context)
