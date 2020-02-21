from lib.db import patch_model

'''
Django启动项目首先加载的是settings.py所在模块（swiper），所以我们需要将patch_model这个函数写在项目的swiper中的__init__.py中
'''

patch_model()