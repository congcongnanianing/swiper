import datetime

from django.db import models

# Create your models here.
from lib.orm import ModelMixin
from social.models import Friend

SEX = (
        ('1','男'),
        ('2','女')
    )


class User(models.Model,ModelMixin):

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

    '''由于多个模型类都需要用到 to_dict 方法，所以我们单独封装一个，通过继承 ModelMixin 来继承这个方法 '''
    # def to_dict(self):
    #     return {
    #         "nickname": self.nickname,
    #         "phonenum":self.phonenums,
    #         "age":self.age,
    #         "sex":self.sex,
    #         "avatar":self.avatar,
    #         "location":self.location
    #     }

    # todo 对外键对优化
    '''
    由于使用外键性能比较差，且不适用于分布式数据库；我们为了达到相同对效果，可以将User和Profile两个类（一对一关系）id保持一致来实现关联。
    
    '''

    @property
    def profile(self):
        # 判断当前对象的_profile属性是否存在
        if not hasattr(self,'_profile'):
            '''由于等号右侧执行的是数据库的操作，效率比较低，假如不将_profile设置为属性，那么执行 _profile.location、_profile.min_distance、_profile.max_distance 对应的是三次数据库的查询，
               加上self.设置为属性后，不管执行多少次 _profile.xxx属性的操作都只进行一次数据库的查询
            '''
            # 这也是一种懒加载的方式，只有当执行user.profile的时候才会执行。get_or_create函数有两个返回值，另外一个不关心所以直接用 "_" 表示
            self._profile, _ = Profile.objects.get_or_create(id=self.id)

        return self._profile

    def friends(self):
        friend_ids_list = Friend.friend_id_list(self.id)
        return User.objects.filter(id__in=friend_ids_list)


class Profile(models.Model,ModelMixin):

    location = models.CharField(max_length=32, verbose_name='目标城市')
    min_distance = models.IntegerField(default=1, verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=10, verbose_name='最大查找范围')
    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=70, verbose_name='最大交友年龄')
    dating_sex = models.CharField(max_length=8, choices=SEX, verbose_name='匹配的性别')
    vibration = models.BooleanField(default=True, verbose_name='是否开启震动')
    only_matche = models.BooleanField(default=True, verbose_name='不让未匹配的人看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='是否自动播放视频')
