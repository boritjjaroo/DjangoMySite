from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

import datetime

from .models import Accounts, CreditCard, Deposit

# =============================================================================
# 가계부 메인
    
def index(request):
    context = {
    }
    return render(request, 'accbook/index.html', context)

# =============================================================================
# 계정과목 관리

# 계정과목을 계층구조로 보여주기 위해 depth-first 방식으로 새 list에 추가하는 함수
def append_child(list, list_ordered, depth, parent_id):
    for account in list:
        if account.depth == depth and account.parent == parent_id:
            list_ordered.append(account)
            if not account.is_slip:
                append_child(list, list_ordered, depth + 1, account.id)


@login_required(login_url='common:login')
def accounts(request):
    scroll_y_pos = request.session.get('_scroll_y_pos')
    if not scroll_y_pos:
        scroll_y_pos = "0"

    accounts_list = Accounts.objects.order_by('depth', 'order')
    accounts_list_ordered = []

    append_child(accounts_list, accounts_list_ordered, 0, None)

    context = {
        'list': accounts_list_ordered,
        'scroll_y_pos': scroll_y_pos,
    }
    return render(request, 'accbook/accounts_list.html', context)

# =============================================================================
# 계정과목 수정
    
@login_required(login_url='common:login')
def accounts_modify(request):
    scroll_y_pos = request.POST.get('scroll_y_pos')
    id = request.POST.get('id')
    if id and id.isdigit():
        account_item = Accounts.objects.filter(id=id).first()
    else:
        account_item = Accounts()

    account_item.depth = request.POST.get('depth')
    parent = request.POST.get('parent')
    if not parent:
        parent = None
    account_item.parent = parent
    account_item.code = request.POST.get('code')
    account_item.name = request.POST.get('name')
    account_item.order = request.POST.get('order')

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

    deposit_id = request.POST.get('deposit')
    if deposit_id:
        deposit = Deposit.objects.get(id=deposit_id)
        if deposit:
            account_item.deposit = deposit

    card_id = request.POST.get('card')
    if card_id:
        card = CreditCard.objects.get(id=card_id)
        if card:
            account_item.card = card

    account_item.save()
    
    request.session['_scroll_y_pos'] = scroll_y_pos
    return redirect('accbook:accounts')

# =============================================================================
# 계좌관리

@login_required(login_url='common:login')
def deposits(request):
    deposits_list = Deposit.objects.order_by('order')

    today = datetime.date.today()
    nearest_item = None
    for item in deposits_list:
        if item.expiration_date and (nearest_item is None or item.expiration_date - today < nearest_item.expiration_date - today):
            nearest_item = item
    
    if nearest_item:
        nearest_item.is_expiration_coming = True;

    context = {
        'list': deposits_list,
    }
    return render(request, 'accbook/deposits.html', context)


# =============================================================================
# 카드관리

@login_required(login_url='common:login')
def credit_card(request):
    card_list = CreditCard.objects.order_by('order')

    today = datetime.date.today()
    nearest_item = None
    for item in card_list:
        if item.valid_date and (nearest_item is None or item.valid_date - today < nearest_item.valid_date - today):
            nearest_item = item
    
    if nearest_item:
        nearest_item.is_expiration_coming = True;

    context = {
        'list': card_list,
    }
    return render(request, 'accbook/creditcard.html', context)
