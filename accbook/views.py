from django.shortcuts import redirect, render
from django.http import HttpResponse

from .models import Accounts

def index(request):
    return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")


def accounts(request):

    accounts_list = Accounts.objects.order_by('order1', 'order2', 'order3')

    context = { 'list': accounts_list }
    return render(request, 'accbook/accounts_list.html', context)

    
def accounts_modify(request):
    id = request.POST.get('id')
    if id and id.isdigit():
        account_item = Accounts.objects.filter(id=id).first()
    else:
        account_item = Accounts()

    account_item.code1 = request.POST.get('code1')
    account_item.name1 = request.POST.get('name1')
    account_item.order1 = request.POST.get('order1')
    account_item.code2 = request.POST.get('code2')
    account_item.name2 = request.POST.get('name2')
    account_item.order2 = request.POST.get('order2')
    account_item.code3 = request.POST.get('code3')
    account_item.name3 = request.POST.get('name3')
    account_item.order3 = request.POST.get('order3')

    date = request.POST.get('begin_date')
    if not date:
        date = None
    account_item.begin_date = date
    date = request.POST.get('end_date')
    if not date:
        date = None
    account_item.end_date = date

    account_item.is_slip = request.POST.get('is_slip') is not None
    account_item.is_temporary = request.POST.get('is_temporary') is not None

    account_item.bank_type = request.POST.get('bank_type')
    account_item.deposit_type = request.POST.get('deposit_type')

    account_item.save()
    
    return redirect('accbook:accounts')
