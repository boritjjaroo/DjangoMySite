from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.db.models import Q

import datetime
from dateutil.relativedelta import relativedelta
from json import JSONEncoder

from .models import *

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
    account_item.is_debit = request.POST.get('is_debit') is not None
    account_item.is_both = request.POST.get('is_both') is not None
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


# =============================================================================
# 월별 관리

@login_required(login_url='common:login')
def monthly(request):
    KST = datetime.timezone(datetime.timedelta(hours=9))
    date_today = datetime.datetime.now(KST)
    acc_year = date_today.year
    acc_month = date_today.month

    account1_list = Accounts.objects.filter(depth=0).order_by('order')
    context = {
        'acc_year': acc_year,
        'acc_month': acc_month,
        'date_today': date_today,
        'account1_list': account1_list,
    }
    return render(request, 'accbook/monthly.html', context)


# =============================================================================
# 전표 등록

def make_slip_data_list(f_accounts, f_amounts, is_debit):
    lists = []
    sum = 0
    for f_account, f_amount in zip(f_accounts, f_amounts):
        try:
            account_id = int(f_account)
            amount = int(f_amount)
            account = Accounts.objects.get(id=account_id)
        except:
            continue
        if account and amount:
            slip_data = SlipData()
            slip_data.account = account
            slip_data.amount = amount
            slip_data.is_debit = is_debit
            lists.append(slip_data)
            sum += amount
    return lists, sum

@login_required(login_url='common:login')
def slip_register(request):
    result = 'Fail'

    is_register_valid = True
    f_date = request.POST.get('f_date') # 2021-11-11T13:25 str type
    if f_date:
        f_date += ' +0900'
    f_desc = request.POST.get('f_desc')
    f_target = request.POST.get('f_target')
    f_d_account = request.POST.getlist('f_d_account[]')
    f_d_amount = request.POST.getlist('f_d_amount[]')
    f_c_account = request.POST.getlist('f_c_account[]')
    f_c_amount = request.POST.getlist('f_c_amount[]')

    try:
        slip_date = datetime.datetime.strptime(f_date, '%Y-%m-%dT%H:%M %z')
    except:
        is_register_valid = False
        print(f'date invalid [{f_date}]')

    debits, sum_debit = make_slip_data_list(f_d_account, f_d_amount, True)
    credits, sum_credit = make_slip_data_list(f_c_account, f_c_amount, False)

    if len(debits) == 0 or len(credits) == 0 or sum_debit != sum_credit:
        is_register_valid = False
        print(f'debits : {sum_debit} {debits}')
        print(f'credits: {sum_credit} {credits}')

    if is_register_valid:
        slip = Slip()
        slip.date = slip_date
        slip.desc = f_desc
        slip.target = f_target
        slip.is_temporary = False
        slip.save()

        for data in debits:
            data.parent = slip
            data.date = slip.date
            data.save()
        for data in credits:
            data.parent = slip
            data.date = slip.date
            data.save()

        result = 'Success'

    print(f'accbook:slip_register : ({result})')
    context = { 'result': result }
    return JsonResponse(context)


# =============================================================================
# 해당 월 전표 목록을 json으로 리턴

class MyJsonEncoderSlip(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            return o.strftime('%m-%d %H:%M')
        if isinstance(o, datetime.datetime):
            return o.strftime('%m-%d %H:%M')
        return o.__dict__

def slip_list(request):
    result = 'Fail'
    result_list = []
    acc_year = request.POST.get('acc_year')
    acc_month = request.POST.get('acc_month')

    try:
        if acc_year:
            acc_year = int(acc_year)
        if acc_month:
            acc_month = int(acc_month)
    except:
        acc_year = None
        acc_month = None

    if acc_year and acc_month:
        KST = datetime.timezone(datetime.timedelta(hours=9))
        date_begin = datetime.datetime(acc_year,acc_month,1,tzinfo=KST)
        date_end = date_begin + relativedelta(months=1)
        slips = Slip.objects.filter(date__gte=date_begin, date__lt=date_end).order_by('date')
        for slip in slips:
            slip_view = SlipView()
            slip_view.slip = slip
            data_list = SlipData.objects.filter(parent=slip)
            for data in data_list:
                data_view = SlipDataView(data)
                slip_view.append(data_view)

            slip_view.calc_count()
            result_list.append(slip_view)
        result = 'Success'
    else:
        print(f'[Error] acc_year({acc_year}), acc_month({acc_month}) is invalid!')

    print(f'accbook:slip_list : ({result}) ({len(result_list)})')
    context = { 'result': result, 'list': result_list }
    return JsonResponse(context, encoder=MyJsonEncoderSlip)


# =============================================================================
# 계정과목 목록을 json으로 리턴

class MyJsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d')
        return o.__dict__

def account_list(request):
    result = 'Fail'
    result_list = []
    depth = request.POST.get('depth')
    parent_id = request.POST.get('parent_id')
    is_debit = request.POST.get('is_debit')
    if is_debit and is_debit == 'true':
        is_debit = True
    else:
        is_debit = False
    print(f'depth=[{depth}] parent_id=[{parent_id}] is_debit=[{is_debit}]')
    
    if depth:
        depth = int(depth)
        query = Q(depth=depth)
        if parent_id:
            parent_id = int(parent_id)
            query.add(Q(parent=parent_id), Q.AND)
        else:
            query.add(Q(parent__isnull=True), Q.AND)
        query.add((Q(is_debit=is_debit) | Q(is_both=True)), Q.AND)

        list = Accounts.objects.filter(query).order_by('order')
        for item in list:
            dict_obj = model_to_dict(item)
            result_list.append(dict_obj)
        result = 'Success'
    context = { 'result': result, 'list': result_list }
    return JsonResponse(context, encoder=MyJsonEncoder)


# =============================================================================
# 1년 통계

@login_required(login_url='common:login')
def annual(request):
    data_list = []
    KST = datetime.timezone(datetime.timedelta(hours=9))
    date_today = datetime.datetime.now(KST)

    acc_year = request.POST.get('acc_year', str(date_today.year))
    acc_year = int(acc_year)
    acc_month = date_today.month

    # 표시할 계정과목 목록 생성
    print('Making annual data account list...')
    accounts = Accounts.objects.order_by('depth', 'order')
    accounts_ordered = []

    append_child(accounts, accounts_ordered, 0, None)

    for account in accounts_ordered:
        annual = AnnualView(account)
        data_list.append(annual)

    # 속도 향상을 위해 dictionary에 추가 저장
    data_list_dic = {}
    asset_index = 0
    debt_index = 0
    capital_index = 0
    for index, data in enumerate(data_list):
        data_list_dic[data.id] = data
        if data.id == Accounts.ASSET:
            asset_index = index
        elif data.id == Accounts.DEBT:
            debt_index = index
        elif data.id == Accounts.CAPITAL:
            capital_index = index

    # 월 단위로 계정과목 금액 계산

    # 작년 이월 월마감 자료 조회
    monthly_last = Monthly.objects.get(year=acc_year-1, month=12)
    monthly_datas = MonthlyData.objects.filter(parent=monthly_last)
    for monthly_data in monthly_datas:
        annual = data_list_dic.get(monthly_data.account_id)
        if annual:
            annual.amounts[AnnualView.LAST] = monthly_data.amount

    print('Calculating Monthly...')
    for month in range(1, 13):
        monthlys = Monthly.objects.filter(year=acc_year, month=month)
        # 월마감이 존재하면 그대로 대입
        if monthlys:
            monthly_last = monthlys[0]
            monthly_datas = MonthlyData.objects.filter(parent=monthly_last)
            for monthly_data in monthly_datas:
                annual = data_list_dic.get(monthly_data.account_id)
                if annual:
                    annual.amounts[month] = monthly_data.amount
        # 월마감이 없을 경우 한 달치 데이터 계산
        else:
            # 대차대조표 계정은 전월 금액에 누적
            for annual in data_list:
                if annual.is_balance:
                    annual.amounts[month] = annual.amounts[month-1]

            date_begin = datetime.datetime(acc_year,month,1,tzinfo=KST)
            date_end = date_begin + relativedelta(months=1)
            slip_datas = SlipData.objects.filter(date__gte=date_begin, date__lt=date_end)

            for slip_data in slip_datas:
                annual = data_list_dic.get(slip_data.account_id)
                if annual:
                    if annual.is_debit == slip_data.is_debit:
                        annual.amounts[month] += slip_data.amount
                    else:
                        annual.amounts[month] -= slip_data.amount

            # 전표미생성 계정의 부분합 구하기
            cur_sum = [0, 0, 0]
            cur_depth = 2
            for annual in reversed(data_list):
                if annual.depth < cur_depth:
                    if annual.is_slip:
                        cur_depth = annual.depth
                        cur_sum[cur_depth] += annual.amounts[month]
                    else:
                        annual.amounts[month] = cur_sum[cur_depth]
                        cur_sum[cur_depth] = 0
                        cur_depth = annual.depth
                        cur_sum[cur_depth] += annual.amounts[month]
                elif annual.depth > cur_depth:
                    if annual.is_slip:
                        cur_depth = annual.depth
                        cur_sum[cur_depth] += annual.amounts[month]
                    else:
                        cur_sum[cur_depth] += annual.amounts[month]
                        cur_depth = annual.depth
                else: # annual.depth == cur_depth
                    cur_sum[cur_depth] += annual.amounts[month]

            # 자본 계정 계산
            data_list[capital_index].amounts[month] = data_list[asset_index].amounts[month] - data_list[debt_index].amounts[month]

            # 손익계산서 계정은 월별 합계를 구한다.
            for annual in data_list:
                if not annual.is_balance:
                    annual.amounts[AnnualView.SUM] += annual.amounts[month]

    print('Calculate sum and avg...')

    for annual in data_list:
        if annual.is_balance:
            annual.amounts[AnnualView.SUM] = annual.amounts[12]
        if 1 < acc_month:
            annual.amounts[AnnualView.AVG] = int(annual.amounts[AnnualView.SUM] / (acc_month - 1))

    context = {
        'acc_year': acc_year,
        'acc_month': acc_month,
        'sum_index': AnnualView.SUM,
        'avg_index': AnnualView.AVG,
        'date_today': date_today,
        'data_list': data_list,
    }
    return render(request, 'accbook/annual.html', context)
