from django.db import models

# Create your models here.
from django.db.models import Q


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
    # dtime = models.DateField(auto_now=True)
    dtime = models.DateTimeField(auto_now=True)

    # todo get_latest_by
    class Meta:
        get_latest_by = 'dtime'

    # todo 对于直接修改model本身的部分 直接在model中添加逻辑； 额外的程序限制之类的逻辑（例如：每日滑动次数、红包之类的）就写在logic里面。

    @classmethod
    def like(cls,uid,sid):
        obj = cls.objects.create(uid=uid,sid=sid,flag='like')
        return obj

    @classmethod
    def superlike(cls, uid, sid):
        obj = cls.objects.create(uid=uid, sid=sid, flag='superlike')
        return obj

    @classmethod
    def dislike(cls, uid, sid):
        obj = cls.objects.create(uid=uid, sid=sid, flag='dislike')
        return obj

    @classmethod
    def is_liked(cls,uid,sid):
        '''检查uid是否喜欢过sid'''
        return cls.objects.filter(uid=uid, sid=sid, flag__in=['like', 'superlike']).exists()

    @classmethod
    def rewind(cls, uid):
        '''撤销操作'''
        # 检查与对方是否为好友关系，如果是好友关系还要删除好友关系

        cls.objects.filter(uid=uid).latest().delete()

    @classmethod
    def liked_me(cls, uid):
        return cls.objects.filter(sid=uid, flag__in=['like', 'superlike'])


class Friend(models.Model):
    '''好友关系表'''
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    @classmethod
    def make_friends(cls,uid1,uid2):
        # 好友关系实际上是平级的，为了在数据库中实现统一，将id小的放在前面，定义下面的逻辑
        # 将id进行排序，在建立关系时就可以避免多次检查 A在前B在后、B在前A在后的逻辑
        uid1, uid2 = sorted([uid1, uid2])

        cls.objects.get_or_create(uid1=uid1, uid2=uid2)

    @classmethod
    def is_friends(cls,uid1,uid2):
        uid1, uid2 = sorted([uid1, uid2])
        return cls.objects.filter(uid1=uid1, uid2=uid2).exists()

    @classmethod
    def break_off_friends(cls,uid1,uid2):
        uid1, uid2 = sorted([uid1, uid2])
        cls.objects.filter(uid1=uid1,uid2=uid2).delete()

    @classmethod
    def friend_id_list(cls, uid):
        '''获取好友的 uid 列表'''
        # 查询我的好友关系
        condition = Q(uid1 = uid) | Q(uid2 = uid)
        relations = cls.objects.filter(condition)
        # 筛选好友的uid
        friend_id_list = list()
        for relation in relations:
            friend_id = relation.uid2 if relation.uid1 == uid else relation.uid1
            friend_id_list.append(friend_id)
        return friend_id_list
