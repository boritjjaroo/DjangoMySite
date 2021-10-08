from django.db import models

# Create your models here.
class Realestate(models.Model):
    address_jibun = models.CharField(max_length=64)
    address_road = models.CharField(max_length=64, default='')
    # 법정동코드
    lawd_cd = models.CharField(max_length=10, default='')
    area = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    building_area = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    total_floor_area = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    # 사용승인일
    use_approval_date = models.DateField(null=True)
    # 주구조
    structure = models.CharField(max_length=16, default='')
    # 난방연료
    heating = models.CharField(max_length=16, default='')
    # 하수처리방식
    sewage = models.CharField(max_length=32, default='')
    # 공시가격
    declared_value = models.IntegerField(default=0)
    declared_value_date = models.DateField(null=True)
    # 실거래가(원)
    deal_price = models.IntegerField(default=0)
    deal_date = models.DateField(null=True)

    is_favorite = models.BooleanField(default=False)
    is_dandok = models.BooleanField(default=False)

    memo = models.CharField(max_length=1024, default='')
    file_prefix = models.CharField(max_length=32, default='')

    def __str__(self) -> str:
        return str(self.address_jibun)

class MyLandItem(models.Model):
    realestate_id = models.BigIntegerField(default=0)
    article_no = models.CharField(max_length=16, unique=True)
    parent_id = models.BigIntegerField(default=0)
    article_confirm_ymd = models.CharField(max_length=16)
    price = models.IntegerField(null=True)
    is_new = models.BooleanField(default=True)
    declared_value = models.IntegerField(null=True)
    declared_value_date = models.DateField(null=True)

    def __str__(self) -> str:
        return str(self.article_no)

class LocationCode(models.Model):
    location = models.CharField(max_length=128)
    code = models.CharField(max_length=16)

    def __str__(self) -> str:
        return str(self.location)
