import datetime

from social.models import Swiped, Friend
from user.models import User


def rcmd_users(user):
    '''推荐用户'''
    dating_sex = user.profile.dating_sex
    location = user.profile.location
    min_dating_age = user.profile.min_dating_age
    max_dating_age = user.profile.max_dating_age

    curr_year = datetime.date.today().year
    min_year = curr_year - max_dating_age
    max_year = curr_year - min_dating_age

    users = User.objects.filter(sex=dating_sex,
                                location=location,
                                birth_year__gte=min_year,
                                birth_year__lte=max_year)

    return users


def like_someone(user,sid):
    Swiped.like(user.id,sid)
    if Swiped.is_liked(sid,user.id):    # 检查对方是否喜欢过自己
        Friend.make_friends(user.id, sid)
        return True
    else:
        return False


def superlike_someone(user,sid):
    Swiped.like(user.id,sid)
    if Swiped.is_liked(sid,user.id):    # 检查对方是否喜欢过自己
        Friend.make_friends(user.id, sid)
        return True
    else:
        return False


def rewind(user):
    '''反悔'''
    # 查出最新的操作记录
    swiped = Swiped.objects.filter(uid=user.id).latest()
    # 删除好友关系
    if swiped.flag in ['like', 'superlike']:
        Friend.break_off_friends(user.id, swiped.sid)
    # 删除滑动记录
    swiped.delete()


def users_liked_me(user):
    swipers = Swiped.liked_me(user.id)
    swipe_uid_list = [u.uid for u in swipers]
    users = User.objects.filter(id__in=swipe_uid_list)
    return users
