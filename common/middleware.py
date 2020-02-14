from django.utils.deprecation import MiddlewareMixin

from common import errors
from lib.http import render_json
from user.models import User


class AuthMiddleware(MiddlewareMixin):

    # 白名单地址，即不需要登录就能访问的路径
    white_list = [
        '/api/user/vcode',
        '/api/user/login',
    ]

    def process_request(self,request):

        # 检查当前path是否在白名单内
        if request.path in self.white_list:
            return

        # 用户登录验证
        uid = request.session.get('uid')
        if not uid:
            return render_json(None,errors.LOGIN_REQUIRED)
        else:
            try:
                user = User.objects.get(id=uid)
            except User.DoesNotExist:
                return render_json(None,errors.USER_NOT_EXIST)
            else:
                # 将user对象添加到 request
                request.user = user
