from django.shortcuts import render

# Create your views here.
from lib.http import render_json
from social.logic import rcmd_users
from social.models import Swiped


def get_rcmd_users(request):
    '''获取推荐列表'''
    user = request.user

    page = int(request.GET.get('page', 1))
    per_page = 10

    start = (page - 1) * per_page
    end = start + per_page

    users = rcmd_users(user)[start:end]
    result = [u.to_dict() for u in users]

    return render_json(result)


def like(request):
    '''喜欢'''
    return render_json(None)


def dislike(request):
    '''不喜欢'''
    return render_json(None)


def superlike(request):
    '''超级喜欢'''
    return render_json(None)


def rewind(request):
    '''反悔'''
    return render_json(None)


def show_liked_me(request):
    '''喜欢我的'''
    return render_json(None)
