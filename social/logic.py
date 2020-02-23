import datetime

from lib.cache import rds
from social.models import Swiped, Friend
from user.models import User
from worker import call_by_worker


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


@call_by_worker
def pre_rcmd(user):
    '''
    推荐预处理
    1. 加载我滑动过的人到缓存，并添加过期时间
    2. 执行推荐算法得到一批用户
    3. 再将取到到用户与缓存中被划过的数据进行去重处理
    4. celery将推荐结果添加到缓存
    '''

    # 将滑动记录添加到redis的set
    swiped = Swiped.objects.filter(uid=user.id).only('sid')
    swiped_sid_list = {s.sid for s in swiped}
    rds.sadd('Swiped-%s' % user.id, *swiped_sid_list)

    # 取出待推荐的用户 id
    rcmd_user_id_list = {u.id for u in rcmd_users(user).only('id')}

    # 去重
    rcmd_user_id_list = rcmd_user_id_list - swiped_sid_list
    rds.sadd('RCMD-%s' % user.id, *rcmd_user_id_list)


def rcmd_users_from_redis(user):
    # 从redis中取出用户id，str类型
    rcmd_user_id_list = [int(id) for id in rds.srandmember('RCMD-%s' % user.id, 10)]
    return User.objects.filter(id__in=rcmd_user_id_list)


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


# todo redis排行榜的实现
def add_swiped_score(uid,flag):
    ''' 添加被滑动的积分记录 '''

    score = {'like': 5, 'superlike': 7, 'dislike': -5}[flag]
    rds.zincrby('Hot-swiped', uid, score)


def get_top_n_swiped(num=10):
    '''获取 Top N 的滑动数据'''
    # 取出并清洗榜单数据
    resource_data = rds.zrevrange('Hot-swiped', 0, num-1, withscores=True)
    cleaned_data = [[int(uid), int(score)] for uid, score in resource_data]

    # 取出用户数据
    uid_list = [uid for uid, _ in cleaned_data]
    users = User.objects.filter(id__in=uid_list)

    # 将users按照 uid_list的顺序排列
    users = sorted(users, key=lambda user:uid_list.index(user.id))

    # 将 cleaned_data 中的uid 替换成user todo zip的使用
    for item, user in zip(cleaned_data, users):
        item[0] = user

    return cleaned_data
