from django.db import models

# Create your models here.
class Accounts(models.Model):
    code1 = models.CharField(max_length=2, default='00')
    name1 = models.CharField(max_length=32, default='')
    order1 = models.IntegerField(default=999)
    code2 = models.CharField(max_length=3, default='000')
    name2 = models.CharField(max_length=32, default='')
    order2 = models.IntegerField(default=999)
    code3 = models.CharField(max_length=3, default='000')
    name3 = models.CharField(max_length=32, default='')
    order3 = models.IntegerField(default=999)

    begin_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    # 전표 발생 가능 여부
    is_slip = models.BooleanField(default=False)

    # 일회성 여부
    is_temporary = models.BooleanField(default=False)

    # 10 : 1금융권
    # 20 : 2금융권
    # 30 : 증권사
    # 90 : 기타
    bank_type = models.CharField(max_length=2, default='00')

    # 10 : 요구불
    # 20 : 정기예금
    # 30 : 정기적금
    # 90 : 기타
    deposit_type = models.CharField(max_length=2, default='00')

    def __str__(self) -> str:
        return str(self.name1) + '-' + str(self.name2) + '-' + str(self.name3)


class Slip(models.Model):
    date = models.DateTimeField()
    desc = models.CharField(max_length=256)

    def __str__(self) -> str:
        return str(self.desc)


class SlipData(models.Model):
    parent = models.ForeignKey(Slip, on_delete=models.CASCADE)
    code = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    is_debit = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.code)
