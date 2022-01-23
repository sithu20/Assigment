from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

class ActivitylogConfig(AppConfig):
    name = 'activitylog'

