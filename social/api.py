from django.shortcuts import render

# Create your views here.
from lib.http import render_json
from social import logic
from social.models import Swiped


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


def like(request):
    '''喜欢'''
    sid = int(request.POST.get('sid'))
    is_matched =logic.like_someone(request.user,sid)

    return render_json({'is_matched':is_matched})


def dislike(request):
    '''不喜欢'''
    sid = int(request.POST.get('sid'))
    Swiped.dislike(request.user.id, sid)
    return render_json(None)


def superlike(request):
    '''超级喜欢'''
    sid = int(request.POST.get('sid'))
    is_matched = logic.superlike_someone(request.user, sid)

    return render_json({'is_matched': is_matched})


def rewind(request):
    '''反悔'''
    logic.rewind(request.user)
    return render_json(None)


def show_liked_me(request):
    '''查看喜欢我的'''
    users = logic.users_liked_me(request.user)
    result = [u.to_dict() for u in users]
    return render_json(result)


def get_friends(request):
    friends = request.user.friends()
    result = [f.to_dict() for f in friends]
    return render_json(result)
