from django.db import models

# Create your models here.
class Realestate(models.Model):
    address_jibun = models.CharField(max_length=64)
    address_road = models.CharField(max_length=64, null=True)
    area = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    building_area = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    total_floor_area = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    # 사용승인일
    use_approval_date = models.DateField(null=True)
    # 주구조
    structure = models.CharField(max_length=16, null=True)
    # 난방연료
    heating = models.CharField(max_length=16, null=True)
    # 하수처리방식
    sewage = models.CharField(max_length=32, null=True)
    # 공시가격
    declared_value = models.IntegerField(null=True)
    declared_value_date = models.DateField(null=True)

    is_favorite = models.BooleanField(default=False)
    memo = models.CharField(max_length=1024, default='')
    file_prefix = models.CharField(max_length=32, null=True)

    def __str__(self) -> str:
        return str(self.address_jibun)

class MyLandItem(models.Model):
    realestate_id = models.BigIntegerField(default=0)
    article_no = models.CharField(max_length=16, unique=True)
    parent_id = models.BigIntegerField(default=0)
    article_confirm_ymd = models.CharField(max_length=16)
    price = models.IntegerField(null=True)
    initial_price = models.CharField(max_length=32, null=True)
    is_multi_family = models.BooleanField(null=True)
    is_new = models.BooleanField(default=True)
    is_favorite = models.BooleanField(default=False)
    memo = models.CharField(max_length=1024, default='')
    declared_value = models.IntegerField(null=True)
    declared_value_date = models.DateField(null=True)

    def __str__(self) -> str:
        return str(self.article_no)

class LocationCode(models.Model):
    location = models.CharField(max_length=128)
    code = models.CharField(max_length=16)

    def __str__(self) -> str:
        return str(self.location)
