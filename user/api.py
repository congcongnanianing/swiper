from django.core.cache import cache
from django.shortcuts import render

# Create your views here.
from common import errors
from lib.http import render_json
from lib.qncloud import upload_to_qiniu
from lib.sms import send_verify_code, check_vcode
from social.logic import pre_rcmd
from user.forms import ProfileForm
from user.logic import save_upload_file, upload_avatar_to_qiniu
from user.models import User


def get_verify_code(request):
    '''获取短信验证码'''
    phonenum = request.GET.get('phonenum')
    send_verify_code(phonenum)

    return render_json(None)


def login(request):
    '''登录'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')

    if not check_vcode(phonenum,vcode):
        user,created = User.get_or_create(phonenums=phonenum)
        request.session['uid'] = user.id

        pre_rcmd(request.user)

        return render_json(user.to_dict('birth_year'))

        # try:
        #     user = User.objects.get()
        # except User.DoesNotExist:
        #     user = User.objects.create()

    else:
        # return render_json(None,errors.VcodeError.code)
        raise errors.VcodeError


def user_back(request):
    '''这个方法用于APP从后台被唤醒的时候调用，触发预推荐异步任务'''
    pre_rcmd(request.user)
    return render_json(None)


def show_profile(request):
    '''查看个人资料'''
    user = request.user

    key = f'Profile-{user.id}'
    result = cache.get(key)

    if result is None:
        result = user.profile.to_dict()
        cache.set(key,result)

    return render_json(result)


def modify_profile(request):
    '''修改个人资料'''
    form = ProfileForm(request.POST)
    if form.is_valid():
        profile = form.save(commit=False)   # 暂时不提交到数据库
        profile.id = request.user.id
        profile.save()
        result = profile.to_dict()

        # 添加缓存
        cache.set(f'Profile-{profile.id}',result)

        return render_json(result)
    else:
        raise errors.ProfileError


def upload_avatar(request):
    avatar = request.FILES.get('avatar')
    # 保存文件到本地
    file_path,file_name = save_upload_file(request.user,avatar)
    # 异步上传文件到七牛
    upload_avatar_to_qiniu(request.user,file_path,file_name)
    return render_json(None)

