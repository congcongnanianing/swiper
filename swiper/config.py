'''除了django配置信息之外的其他配置信息存在这里'''

# 互亿无线短信平台配置
HY_SMS_URL = 'https://106.ihuyi.com/webservice/sms.php?method=Submit'
HY_SMS_PARAMS = {
    "account":'C98788114',
    "password":'4a762cfd50edab92feefc4eea8c9a06b',
    "content":'您的验证码是：%s，请不要把验证码泄漏给其他人。',
    "mobile":None,
    "format":'json'
}


# 七牛云的配置
QN_ACCESS_KEY = 'lkVxkXBT43HMnuZJ7k_ivEwN8Ms4uUa-HimZzWE9'
QN_SECRET_KEY = 'ssaupRt245ndv7mQXMmq2s1JI-8lEFZ1xI-801kU'
QN_BASE_URL = 'http://q5q9vqbal.bkt.clouddn.com'
QN_BUCKET = 'swiper-cy'
