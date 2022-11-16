DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # engine: mysql
        'NAME' : 'battery', # DB Name
        'USER' : 'admin', # DB User
        'PASSWORD' : 'rkddbqls12', # Password
        'HOST': 'battery.cq1z58a6la88.ap-northeast-2.rds.amazonaws.com', # 생성한 데이터베이스 엔드포인트
        'PORT': '3306', # 데이터베이스 포트
        'OPTIONS':{
            'init_command' : "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}