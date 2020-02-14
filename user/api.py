from django.shortcuts import render

# Create your views here.
from common import errors
from lib.http import render_json
from lib.sms import send_verify_code, check_vcode
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
        user,created = User.objects.get_or_create(phonenums=phonenum)
        request.session['uid'] = user.id

        return render_json(user.to_dict('birth_year'))

        # try:
        #     user = User.objects.get()
        # except User.DoesNotExist:
        #     user = User.objects.create()

    else:
        return render_json(None,errors.VCODE_ERROR)


def show_profile(request):

    user = request.user

    return render_json(user.profile.to_dict())


def modify_profile(request):
    return


def upload_avatar(request):
    return

