import os

from celery import Celery

from worker import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swiper.settings")

celery_app = Celery('swiper')
celery_app.config_from_object(config)   # 加载配置
celery_app.autodiscover_tasks() # 自动去django中找任务


def call_by_worker(func):
    ''' 在celery中对任务进行异步调用 '''
    # 这种写法也可以看成装饰器（满足一进一出都是函数）。在需要异步执行的函数上加上这个装饰器即可，这样就不需要去修改函数调用的地方为delay模式了。
    task = celery_app.task(func)
    return task.delay
