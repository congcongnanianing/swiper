import os

from django.conf import settings

from lib.qncloud import upload_to_qiniu
from worker import call_by_worker


def save_upload_file(user,upload_file):
    ''' 将上传的文件保存到本地'''

    file_name = 'avatar_%s' % user.id
    file_path = os.path.join(settings.BASE_DIR,settings.MEDIA_ROOT,file_name)

    with open(file_path,'wb') as fb:

        for chunk in upload_file.chunks():
            fb.write(chunk)

    return file_path,file_name


@call_by_worker
def upload_avatar_to_qiniu(user,file_path,file_name):
    ''' 将用户头像上传到七牛云 '''

    *_, avatar_url = upload_to_qiniu(file_path,file_name)
    user.avatar = avatar_url
    user.save()
