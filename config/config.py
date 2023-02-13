import os

class ConfigClass(object):
    """docstring for ."""
    API_HOST_DOMAIN = os.getenv("API_HOST_DOMAIN","0.0.0.0")
    API_HOST_PORT = int(os.getenv("API_PORT",8000))
    RELOAD_CODE = os.getenv("RELOAD_CODE",True)
    NUMBER_OF_WORKER = int(os.getenv("NUMBER_OF_WORKER",4))
    APP_TOKEN = os.getenv("APP_TOKEN",'apptoken')
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER",'redis://redis:6379/0')
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND",'redis://redis:6379/0')

    # CALL_PER_ONE_MINUTE = int(os.getenv("CALL_PER_ONE_MINUTE",80))
    # ENV = os.getenv("APP_ENV",'localhost')
    # DB_PREFIX = os.getenv("DB_PREFIX","finan_dev_ms")

    # def get_FINAN_DB_READ_URL(self, db_name=None):
    #     if db_name is None:
    #         db = os.getenv("FINAN_DB_DB")
    #     else: db = self.DB_PREFIX + '_' + db_name
    #     return '{driver}://{user}:{password}@{host}:{port}/{db}'.format(
    #         driver = os.getenv("FINAN_DB_DRIVER","postgresql+psycopg2"),
    #         user = os.getenv("FINAN_DB_USER"), password = os.getenv("FINAN_DB_PASS"),
    #         host = os.getenv("FINAN_DB_HOST"), port = os.getenv("FINAN_DB_PORT"), db = db
    #     )

    def get_DB_URL(self, db_name=None):
        if db_name is None:
            db = os.getenv("DWH_DB_DB")
        else: db = db_name
        return '{driver}://{user}:{password}@{host}:{port}/{db}'.format(
            driver = os.getenv("DWH_DB_DRIVER","postgresql+psycopg2"),
            user = os.getenv("DWH_DB_USER"), password = os.getenv("DWH_DB_PASS"),
            host = os.getenv("DWH_DB_HOST"), port = os.getenv("DWH_DB_PORT"), db = db
        )

    # def get_VIETTEL_DB_URL(self, db_name=None):
    #     if db_name is None:
    #         db = os.getenv("VIETTEL_DB_DB")
    #     else: db = db_name
    #     return '{driver}://{user}:{password}@{host}:{port}/{db}'.format(
    #         driver = os.getenv("VIETTEL_DB_DRIVER","postgresql+psycopg2"),
    #         user = os.getenv("VIETTEL_DB_USER"), password = os.getenv("VIETTEL_DB_PASS"),
    #         host = os.getenv("VIETTEL_DB_HOST"), port = os.getenv("VIETTEL_DB_PORT"), db = db
    #     )

    DWH_DB_SCHEMA = os.getenv("DWH_DB_SCHEMA","production")
    # DWH_DB_VIETTEL = 'viettel'
    # DWH_DB_CDP = 'cdp'
    # DWH_DB_PII_NAME = 'finan_pii'
    DWH_TIMEZONE = 'Asia/Ho_Chi_Minh'
    DWH_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    # BIGQUERY_PROJECT_ID = 'finan-1ae3f'
    # DWH_DB_NAME = 'finan'
    # DWH_TIMEZONE = 'Asia/Ho_Chi_Minh'
    # DWH_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    # NOTI_DELTA_MINS = int(os.getenv("NOTI_DELTA_MINS",120))

    # FINAN_BACKEND_API_DOMAIN = os.getenv("FINAN_BACKEND_API_DOMAIN",'https://dev-api.finan.cc')
    # FINAN_BACKEND_API_TOKEN = os.getenv("FINAN_BACKEND_API_TOKEN",'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NjQ1Mz')

    # GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS" ,'/Users/datle/code/dp-engine/credentials/SA_bigquery_credentials.json')

    # SHOPEE_API_KEY = 'c54f768645e9ae3c6a33290ca587ccd574acb0f15ff3fe7e8664e4b5535b5cf2'
    # SHOPEE_PARTNER_ID = 2000512

    # BOTPRESS_DOMAIN = os.getenv("BOTPRESS_DOMAIN","https://bi.finan.me")
    # BOT_ID = os.getenv("BOT_ID","sbh-development-bot")

    # MIXPANEL_USER = os.getenv("MIXPANEL_USER","bi2.705b99.mp-service-account")
    # PUSH_EVENT_TO_MIXPANEL = os.getenv("PUSH_EVENT_TO_MIXPANEL", False)
    # MIXPANEL_SECRECT = os.getenv("MIXPANEL_SECRECT","yOWgeX8rPX9oFvy0VsylXPwTvqqthqiz")
    # MIXPANEL_PROJECT_ID = os.getenv("MIXPANEL_PROJECT_ID",2453399)
    # MIXPANEL_API_KEY = os.getenv("MIXPANEL_API_KEY",'0e65044597a1ee05c8d0796a3d2fb4ee')
    # MIXPANEL_API_SECRET = os.getenv("MIXPANEL_API_SECRET",'8865b15a800d1d5f121c95bded8ac8f7')


config = ConfigClass()
