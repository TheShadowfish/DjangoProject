from django.apps import AppConfig
import time



class MailappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailapp'

    def ready(self):
        # if crontab_is_started == False:
        from .utils.utils import start
        time.sleep(30)
        # crontab_is_started = True
        print("crontab_is_started = True")
        start()
