from django.db import models

# Create your models here.


class Swiped(models.Model):

    '''滑动记录'''

    FLAGES = (
        ('superlike','上滑'),
        ('like','右滑'),
        ('dislike','左滑'),
    )

    uid = models.IntegerField(verbose_name='滑动者id')
    sid = models.IntegerField(verbose_name='被滑动者id')
    flag = models.CharField(max_length=10,choices=FLAGES,verbose_name='滑动类型')
    dtime = models.DateField(auto_now=True)


class Friend(models.Model):
    '''好友关系表'''
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()
