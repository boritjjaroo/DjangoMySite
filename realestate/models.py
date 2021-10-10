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

class Address(models.Model):
    # 법정동코드
    lawd_cd = models.CharField(max_length=10, default='')
    # 시도
    sido = models.CharField(max_length=16, default='')
    # 시군구
    sigungu = models.CharField(max_length=16, default='')
    # 읍면
    eupmyun = models.CharField(max_length=16, default='')
    # 리명
    ri = models.CharField(max_length=16, default='')
    # 산여부
    # 0: 일반, 1: 산
    is_san = models.IntegerField(default=0)
    # 지번본번
    jibun_bonbun = models.IntegerField(default=0)
    # 지번부번
    jibun_bubun = models.IntegerField(default=0)
    # 도로명코드
    road_cd = models.CharField(max_length=12, default='')
    # 도로명
    road = models.CharField(max_length=16, default='')
    # 건물번호본번
    road_bonbun = models.IntegerField(default=0)
    # 건물번호부번
    # 없을 경우 값이 0 임
    road_bubun = models.IntegerField(default=0)
    # 건물관리번호
    # 법정동코드(10) + 산여부(1) + 지번본번(4) + 지번부번(4) + 시스템번호(6)
    house_cd = models.CharField(max_length=25, default='')

    def jibun_address(self):
        address = self.sido + ' ' + self.sigungu + ' ' + self.eupmyun
        if self.ri:
            address += ' ' + self.ri
        if self.jibun_bonbun:
            address += ' ' + str(self.jibun_bonbun)
        if self.jibun_bubun:
            address += '-' + str(self.jibun_bubun)
        return address

    def __str__(self) -> str:
        return str(self.location)

if __name__ == "__main__":
    address = Address()
    address.sido = "경상남도"
    address.sigungu = "양산시"
    address.eupmyun = '물금읍'
    address.ri = '범어리'
    address.jibun_bonbun = 538
    address.jibun_bubun = 1
    print(address.jibun_address())
