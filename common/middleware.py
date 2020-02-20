from sys import exc_info
from traceback import format_exception

from django.utils.deprecation import MiddlewareMixin

from common import errors
from lib.http import render_json
from user.models import User


# todo django本身自带的Auth耦合性太强，我们这里使用自己自定义的（主要是为了将user添加到request上）
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
            return render_json(None,errors.LoginRequired.code)
        else:
            try:
                user = User.objects.get(id=uid)
            except User.DoesNotExist:
                return render_json(None,errors.UserNotExist.code)
            else:
                # 将user对象添加到 request
                request.user = user


class LogicErrorMiddleware(MiddlewareMixin):
    def process_exception(self,request,exception):
        '''异常处理'''
        if isinstance(exception,errors.LogicError):
            # 处理逻辑错误
            return render_json(None,exception.code)
        # else:
        #     # 处理程序错误
        #     error_info = format_exception(*exc_info())
