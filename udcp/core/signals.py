import logging

from .models import UserLoginAudit
# for logging - define "error" named logging handler and logger in settings.py
from django.contrib.auth import user_logged_in, user_login_failed
from django.dispatch import receiver





