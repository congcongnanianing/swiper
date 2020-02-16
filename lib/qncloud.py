from urllib.parse import urljoin

from qiniu import Auth, put_file, etag
from swiper import config

# 需要填写你的 Access Key 和 Secret Key
from worker import call_by_worker

access_key = config.QN_ACCESS_KEY
secret_key = config.QN_SECRET_KEY

# 构建鉴权对象
q = Auth(access_key, secret_key)

# 要上传的空间
bucket_name = config.QN_BUCKET


# 获取七牛上到文件路径
def get_qn_url(filename):
    # todo urljoin用法
    return urljoin(config.QN_BASE_URL,filename)


def upload_to_qiniu(localfile,key):
    '''
        将本地文件上传到七牛云：
        localfile：本地文件位置
        key：上传到云服务器后的文件名
    '''

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    ret, info = put_file(token, key, localfile)

    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)

    url = get_qn_url(key)

    return ret, info, url


# 异步函数，依赖于celery，中间过程不好监控，用于非调试模式；上面那个可以没有celery直接调用。
async_upload_to_qiniu = call_by_worker(upload_to_qiniu)



