from django.db import models

# Create your models here.
class MyLandItem(models.Model):
    article_no = models.CharField(max_length=16, unique=True)
    article_confirm_ymd = models.CharField(max_length=16)
    is_multi_family = models.BooleanField(null=True)
    is_new = models.BooleanField(default=True)
    is_favorite = models.BooleanField(default=False)
    memo = models.CharField(max_length=1024, default='')

    def __str__(self) -> str:
        return str(self.article_no)

class LocationCode(models.Model):
    location = models.CharField(max_length=128)
    code = models.CharField(max_length=16)

    def __str__(self) -> str:
        return str(self.location)
