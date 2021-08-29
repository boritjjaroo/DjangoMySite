from django.shortcuts import render
from django.http import HttpResponse
from .models import MMDList, MMDMovie
from django.core.paginator import Paginator


def index(request):
    page = request.POST.get('page', '1')
    per_page = request.POST.get('per_page', '10')

    result_list = MMDMovie.objects.order_by('id')

    paginator = Paginator(result_list, per_page)
    page_obj = paginator.get_page(page)

    per_page_list = (10, 20, 30, 50, 100)

    context = { 'list': page_obj, 'per_page_list': per_page_list }
    return render(request, 'mmd/list.html', context)
