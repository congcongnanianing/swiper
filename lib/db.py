from django.core.cache import cache
from django.db import models

'''对Model的一些方法的封装，monkey patch 设置缓存'''


def get(cls, *args, **kwargs):
    '''数据优先从缓存中获取，缓存中取不到再从数据库中取'''

    # 创建key
    pk = kwargs.get('pk') or kwargs.get('id')

    # 从缓存中获取
    if pk is not None:
        key = 'Model:%s:%s' % (cls.__name__, pk)
        model_obj = cache.get(key)
        print('get from cache: %s' % model_obj)
        if isinstance(model_obj, cls):
            return model_obj

    # 缓存里没有，直接从数据库获取，同时写入缓存
    model_obj = cls.objects.get(*args, **kwargs)
    print('get from db: %s' % model_obj)
    key = 'Model:%s:%s' % (cls.__name__, model_obj.pk)
    cache.set(key, model_obj, 604800)   # 缓存一周时间
    print('set to cache')
    return model_obj


def get_or_create(cls, *args, **kwargs):
    '''数据优先从缓存中获取，缓存中取不到再从数据库中取'''

    # 创建key
    pk = kwargs.get('pk') or kwargs.get('id')

    # 从缓存中获取
    if pk is not None:
        key = 'Model:%s:%s' % (cls.__name__, pk)
        model_obj = cache.get(key)

        print('get from cache: %s' % model_obj)

        if isinstance(model_obj, cls):
            return model_obj, False     # 返回值False表示不是create，而是从缓存中取得。

    # 执行原生方法并添加缓存
    model_obj, created = cls.objects.get_or_create(*args, **kwargs)

    print('get from db: %s' % model_obj)

    key = 'Model:%s:%s' % (cls.__name__, model_obj.pk)
    cache.set(key, model_obj, 604800)   # 缓存一周时间

    print('set to cache')

    return model_obj, created


def save_with_cache(model_save_func):
    def save(self, *args, **kwargs):
        '''存入数据后，同时写入缓存'''
        # 调用原生的 Model.save() 将数据保存到数据库
        model_save_func(self, *args, **kwargs)
        # 添加缓存
        key = 'Model:%s:%s' % (self.__class__.__name__, self.pk)
        cache.set(key, self, 604800)
    return save


def to_dict(self, *ignore_fields):
    '''将 model 转换成字典'''
    attr_dict = dict()
    for field in self._meta.fields: # 遍历所有字段
        name = field.attname    # 取出字段名称
        if name not in ignore_fields:   # 检查是否是需要忽略的字段
            attr_dict[name] = getattr(self,name)    # 获取字段对应的值
    return attr_dict


# todo 修改原生Model中的若干方法
def patch_model():
    '''
    动态更新 Model方法
    Model在 Django中是一个特殊的类,如果通过继承的方式来增加或修改原有方法, Django会将
    继承的类识别为一个普通的app.modeL,所以只能通过 monkey patch的方式动态修改。

    Django启动项目首先加载的是settings.py所在模块（swiper），所以我们需要将patch_model这个函数写在项目的swiper中的__init__.py中。

    '''

    # 动态添加类方法get,get_or_create
    models.Model.get = classmethod(get)
    models.Model.get_or_create = classmethod(get_or_create)

    # 修改save
    models.Model.save = save_with_cache(models.Model.save)

    # 添加to_dict，这样之前写在lib/orm.py中的to_dict就可以不用了，模型类中也不需要再继承ModelMixin
    models.Model.to_dict = to_dict

