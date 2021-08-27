from django.db import models

# Create your models here.
class MMDList(models.Model):
    title = models.CharField(max_length=256)
    # 보카로 가사위키 정보 기준
    song_title = models.CharField(max_length=256)
    song_composer = models.CharField(max_length=128)
    # 한글 명칭 우선하고 없을 경우 원어 사용, 복수 일 경우 콤마로 구분
    character = models.CharField(max_length=256)
    creator = models.CharField(max_length=128)
    url = models.CharField(max_length=512)
    saved_url = models.CharField(max_length=512, null=True)
    lyrics_url = models.CharField(max_length=512, null=True)

    def __str__(self) -> str:
        return str(self.title)
