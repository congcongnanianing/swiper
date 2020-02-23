from django.shortcuts import render

# Create your views here.
from lib.cache import rds
from lib.http import render_json
from social import logic
from social.models import Swiped
from vip.logic import need_perm


def get_rcmd_users(request):
    '''获取推荐列表'''
    user = request.user

    page = int(request.GET.get('page', 1))
    per_page = 10

    start = (page - 1) * per_page
    end = start + per_page

    users = logic.rcmd_users(user)[start:end]
    result = [u.to_dict() for u in users]

    return render_json(result)


def get_rcmd_users_redis(request):
    '''新的基于 Redis 的推荐处理'''
    # 不再需要使用分页了，直接每次从set中随机取出10个用户id
    users =logic.rcmd_users_from_redis(request.user)
    result = [u.to_dict() for u in users]

    return render_json(result)


def like(request):
    '''喜欢'''
    sid = int(request.POST.get('sid'))
    is_matched =logic.like_someone(request.user,sid)

    # 积分
    logic.add_swiped_score(sid, 'like')

    rds.srem('RCMD-%s' % request.user.id, sid)

    return render_json({'is_matched':is_matched})


def dislike(request):
    '''不喜欢'''
    sid = int(request.POST.get('sid'))
    Swiped.dislike(request.user.id, sid)

    logic.add_swiped_score(sid, 'dislike')
    rds.srem('RCMD-%s' % request.user.id, sid)

    return render_json(None)


@need_perm('superlike')
def superlike(request):
    '''超级喜欢'''
    sid = int(request.POST.get('sid'))
    is_matched = logic.superlike_someone(request.user, sid)

    logic.add_swiped_score(sid, 'superlike')
    rds.srem('RCMD-%s' % request.user.id, sid)

    return render_json({'is_matched': is_matched})


@need_perm('rewind')
def rewind(request):
    '''反悔'''
    logic.rewind(request.user)
    return render_json(None)


@need_perm('show_liked_me')
def show_liked_me(request):
    '''查看喜欢我的'''
    users = logic.users_liked_me(request.user)
    result = [u.to_dict() for u in users]
    return render_json(result)


def get_friends(request):
    friends = request.user.friends()
    result = [f.to_dict() for f in friends]
    return render_json(result)


def hot_swiped(request):
    '''排行榜用户'''
    data = logic.get_top_n_swiped(10)

    for item in data:
        item[0] = item[0].to_dict()

    return render_json(data)
