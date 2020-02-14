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