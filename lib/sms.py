import random

import requests
from django.core.cache import cache

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
def send_verify_code(phonenum):
    ''' 发送验证码 '''
    vcode = gen_verify_code()
    
    print('<<<<<<<<<<vcode>>>>>>>>>: %s' % vcode)

    params = config.HY_SMS_PARAMS.copy()    # 用字典的copy方法，只针对局部进行修改
    params['mobile'] = phonenum
    params['content'] = params['content'] % vcode
    #
    # import time
    # time.sleep(30)
    # print('async task finished')
    # response = None

    response = requests.post(config.HY_SMS_URL,data=params)

    cache.set('VCode-%s' % phonenum,vcode,60)

    return response


def check_vcode(phonenum,vcode):
    cache_code = cache.get('VCode-%s' % phonenum)
    return cache_code == vcode
