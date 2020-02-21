

# 这个方法被lib/db.py中的to_dict取代，通过maonkey patch 方式直接修改原生的Nodel，给原生Model增加这个方法
'''

class ModelMixin:
    # 由于很多模型类都需要 to_dict方法，所以我们这里将它抽取出来避免冗余的代码
    def to_dict(self,ignore_fields=()):
        # 将 model 转换成字典
        attr_dict = dict()
        for field in self._meta.fields: # 遍历所有字段
            name = field.attname    # 取出字段名称
            if name not in ignore_fields:   # 检查是否是需要忽略的字段
                attr_dict[name] = getattr(self,name)    # 获取字段对应的值
        return attr_dict

'''