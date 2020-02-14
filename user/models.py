import datetime

from django.db import models

# Create your models here.

SEX = (
        ('1','男'),
        ('2','女')
    )


class User(models.Model):

    nickname = models.CharField(max_length=32,unique=True)
    phonenums = models.CharField(max_length=16,unique=True)
    sex = models.CharField(max_length=8,choices=SEX)
    birth_year = models.IntegerField(default=2000,verbose_name='出生年')
    birth_month = models.IntegerField(default=1,verbose_name='出生月')
    birth_day = models.IntegerField(default=1,verbose_name='出生日')
    avatar = models.CharField(max_length=256,verbose_name='个人形象')
    location = models.CharField(max_length=32,verbose_name='常居地')

    @property
    def age(self):
        # 用户的年龄
        now_day = datetime.date.today()
        birth_day = datetime.date(self.birth_year,self.birth_month,self.birth_day)
        return (now_day - birth_day).days // 365

    def to_dict(self):
        return {
            "nickname": self.nickname,
            "phonenum":self.phonenums,
            "age":self.age,
            "sex":self.sex,
            "avatar":self.avatar,
            "location":self.location
        }


class Profile(models.Model):

    location = models.CharField(max_length=32,verbose_name='目标城市')
    min_distance = models.IntegerField(default=1,verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=10,verbose_name='最大查找范围')
    min_dating_age = models.IntegerField(default=18,verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=70,verbose_name='最大交友年龄')
    dating_sex = models.CharField(max_length=8,choices=SEX,verbose_name='匹配的性别')
    vibration = models.BooleanField(default=True,verbose_name='是否开启震动')
    only_matche = models.BooleanField(default=True,verbose_name='不让未匹配的人看我的相册')
    auto_play = models.BooleanField(default=True,verbose_name='是否自动播放视频')
