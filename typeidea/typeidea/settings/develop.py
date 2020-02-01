from .base import *

DEBUG = True
# DEBUG = False
# ALLOWED_HOSTS = ['*', ]

DATABASES = {
        'default':{
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
        }

        # 'default': {
        #     'ENGINE': 'django.db.backends.mysql',
        #     'NAME': 'typeidea_db',
        #     'USER': 'root',
        #     'PASSWORD': 'qiujie',
        #     'HOST': '127.0.0.1',
        #     'PORT': 3306,
        #     # 'CONN_MAX_AGE': 5*60,
        #     # 'OPTIONS': {'charset': 'utf8mb4'}
        # }

}


""" 使用 diango-debug-toolbar 进行优化调试 DEBUG = True 生效 """
#
# INSTALLED_APPS += [
#     'debug_toolbar',
# ]
#
# MIDDLEWARE += [
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# ]
# INTERNAL_IPS = ['127.0.0.1']
#

