import random

import requests
from django.core.cache import cache

from common.errors import VcodeExist
from swiper import config
from worker import call_by_worker


def gen_verify_code(length=6):
    '''产生验证码'''

    # 100000   999999
    min_value = 10 ** (length-1)
    max_value = 10 ** length

    num = random.randrange(min_value,max_value)

    return num


@call_by_worker
def send_sms(phonenum,msg):
    '''发送短信'''
    params = config.HY_SMS_PARAMS.copy()  # 用字典的copy方法，只针对局部进行修改
    params['mobile'] = phonenum
    params['content'] = params['content'] % msg

    response = requests.post(config.HY_SMS_URL, data=params)

    return response


def send_verify_code(phonenum):
    ''' 发送验证码 '''

    key = 'VCode-%s' % phonenum

    if not cache.has_key(key):
        vcode = gen_verify_code()
        send_sms(phonenum,vcode)
        cache.set(key,vcode,300)
        print('>>>>>>>> vcode: %d' %vcode)
    else:
        raise VcodeExist


def check_vcode(phonenum,vcode):
    cache_code = cache.get('VCode-%s' % phonenum)
    print(cache_code)
    print(vcode)
    return cache_code == vcode
