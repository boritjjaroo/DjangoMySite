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

class VocaloidSong(models.Model):
    title = models.CharField(max_length=256)
    composer = models.CharField(max_length=128)
    lyrics_url = models.CharField(max_length=512, null=True)

    def __str__(self) -> str:
        return str(self.title)

class MMDCharacter(models.Model):
    name = models.CharField(max_length=32)
    name_original = models.CharField(max_length=32)
    name_eng = models.CharField(max_length=32)

    def __str__(self) -> str:
        return str(self.name)

class MMDModel(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self) -> str:
        return str(self.name)

class MMDMaker(models.Model):
    name = models.CharField(max_length=32)
    url = models.CharField(max_length=512, null=True)

    def __str__(self) -> str:
        return str(self.name)

class MMDMovie(models.Model):
    title = models.CharField(max_length=256)
    song = models.ForeignKey(VocaloidSong, on_delete=models.CASCADE)
    character = models.ForeignKey(MMDCharacter, on_delete=models.CASCADE)
    model = models.ForeignKey(MMDModel, on_delete=models.CASCADE)
    maker = models.ForeignKey(MMDMaker, on_delete=models.CASCADE)
    url_type = models.CharField(max_length=16, default='youtube')
    url = models.CharField(max_length=512)
    saved_url = models.CharField(max_length=512, null=True)

    def __str__(self) -> str:
        return str(self.title)

