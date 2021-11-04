from django.db import models

FnInst_Types = {
    1: '1금융권',
    2: '2금융권',
    3: '증권사',
    4: '카드사',
    999: '기타',
}

Deposit_Types = {
    1: '수시입출금',
    2: '정기예금',
    3: '정기적금',
    4: 'ISA',
    5: '연금저축',
    999: '기타',
}

Card_Types = {
    1: '체크',
    2: '신용',
    3: '선불',
    4: '더미',
    999: '기타',
}

IntnCard_Types = {
    1: 'Visa',
    2: 'Master',
    3: 'UnionPay',
    4: 'JCB',
    5: 'BC',
    999: '없음',
}

# =============================================================================
# 금융기관


class FnInst(models.Model):
    name = models.CharField(max_length=32, default='')
    type = models.IntegerField(default=999)
    order = models.IntegerField(default=999)

    @property
    def type_str(self):
        return FnInst_Types[self.type]

    def __str__(self) -> str:
        return str(self.name1)


# =============================================================================
# 계좌
class Deposit(models.Model):
    fn_inst = models.ForeignKey(FnInst, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, default='')
    number = models.CharField(max_length=32, default='')
    type = models.IntegerField(default=999)
    is_protected = models.BooleanField(default=False)
    state = models.CharField(max_length=32, default='정상')
    interest_rate = models.CharField(max_length=32, default='')
    # 개설일
    begin_date = models.DateField(null=True)
    # 해지일
    end_date = models.DateField(null=True)
    # 만기일
    expiration_date = models.DateField(null=True)
    # 설명
    description = models.CharField(max_length=1024, default='')
    order = models.IntegerField(default=999)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_expiration_coming = False

    @property
    def type_str(self):
        return Deposit_Types[self.type]

    def __str__(self) -> str:
        return str(self.name)


# =============================================================================
# 카드
class CreditCard(models.Model):
    fn_inst = models.ForeignKey(FnInst, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, default='')
    number = models.CharField(max_length=32, default='')
    type = models.IntegerField(default=999)
    intn_type = models.IntegerField(default=999)
    state = models.CharField(max_length=32, default='정상')
    is_trans = models.BooleanField(default=False)
    is_cash = models.BooleanField(default=False)
    fee = models.IntegerField(default=0)
    # 발급일
    begin_date = models.DateField(null=True)
    # 해지일
    end_date = models.DateField(null=True)
    # 유효기간
    valid_date = models.DateField(null=True)
    # 결제 계좌
    deposit = models.ForeignKey(Deposit, on_delete=models.SET_NULL, null=True)
    # 설명
    description = models.CharField(max_length=1024, default='')
    order = models.IntegerField(default=999)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_expiration_coming = False

    @property
    def type_str(self):
        return Card_Types[self.type]

    @property
    def intn_type_str(self):
        return IntnCard_Types[self.intn_type]

    def __str__(self) -> str:
        return str(self.name)


# =============================================================================
# 계정과목
class Accounts(models.Model):
    depth = models.IntegerField(default=0)
    parent = models.BigIntegerField(null=True)
    name = models.CharField(max_length=32, default='')
    order = models.IntegerField(default=999)

    begin_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    # 전표 발생 가능 여부
    is_slip = models.BooleanField(default=False)

    # 일회성 여부
    is_temporary = models.BooleanField(default=False)

    # 차변, 대변 발생 여부
    is_debit = models.BooleanField(default=False)
    is_both = models.BooleanField(default=False)

    deposit = models.ForeignKey(Deposit, on_delete=models.SET_NULL, null=True)
    card = models.ForeignKey(CreditCard, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return str(self.name)


# =============================================================================
# 전표
class Slip(models.Model):
    date = models.DateTimeField()
    target = models.CharField(max_length=32, default='')
    desc = models.CharField(max_length=256, default='')
    # 일회성 여부
    is_temporary = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.desc)


# =============================================================================
# 전표항목
class SlipData(models.Model):
    parent = models.ForeignKey(Slip, on_delete=models.CASCADE)
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    amount = models.BigIntegerField(default=0)
    # 차변 여부
    is_debit = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.account.name)

# =============================================================================
# 전표(데이터 처리용)


class SlipDataView:
    def __init__(self, slip_data):
        self.id = slip_data.id
        self.account_id = slip_data.account.id
        self.account_name = slip_data.account.name
        self.amount = slip_data.amount
        self.is_debit = slip_data.is_debit

    def __str__(self) -> str:
        return str(self.account_name)


class SlipView:
    def __init__(self):
        self.slip = None
        self.debits = []
        self.credits = []
        self.rows = 1

    def append(self, data_view):
        if data_view.is_debit:
            self.debits.append(data_view)
        else:
            self.credits.append(data_view)

    def calc_count(self):
        self.rows = max([1, len(self.debits), len(self.credits)])

    def __str__(self) -> str:
        return str(self.slip.desc)
