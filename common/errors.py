OK = 0
VCODE_ERROR = 1000
LOGIN_REQUIRED = 1001
USER_NOT_EXIST = 1002
PROFILE_ERROR = 1003


class LogicError(Exception):
    code = 0

    def __str__(self):
        return self.__class__.__name__


# todo 利用type动态创建逻辑异常类
def generate_logic_error(name,code):
    return type(name,(LogicError,),{'code':code})


OK = generate_logic_error('OK', 0)
VcodeError = generate_logic_error('VcodeError', 1000)
VcodeExist = generate_logic_error('VcodeExist',1001)
LoginRequired = generate_logic_error('LoginRequired', 1002)
UserNotExist = generate_logic_error('UserNotExist', 1003)
ProfileError = generate_logic_error('ProfileError', 1004)
HasNotPerm = generate_logic_error('HasNotPerm', 1005)
