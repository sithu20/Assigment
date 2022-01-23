from django.db import models
from django.contrib.auth.models import User, Group

class UserProfile(models.Model):
    TITLE_CHOICES = (
        ('MR', 'MR'),
        ('MS', 'MS'),
        ('MRS', 'MRS'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=10, choices=TITLE_CHOICES, blank=True, null=True)
    mobileno = models.CharField(max_length=255, blank=True,null=True)
    memcode = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='userprofile', blank=True, null=True)

    def __str__(self):
        return self.user.username

class UserOccupation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ocpName = models.CharField(max_length=100,blank=True, null=True)
    ocpSalary = models.CharField(blank=True,max_length=100)
    createBy = models.CharField(max_length=100,blank=True, null=True)
    createDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.user.username, self.ocpName, self.ocpSalary)


class UserLoginAudit(models.Model):
    # Login Status
    SUCCESS = 'S'
    FAILED = 'F'

    LOGIN_STATUS = ((SUCCESS, 'Success'),(FAILED, 'Failed'))

    ip = models.GenericIPAddressField(null=True)
    username = models.CharField(max_length=256, null=True)
    emailaddress = models.CharField(max_length=256, null=True)
    user_agent_info = models.CharField(max_length=255,  null=True)
    status = models.CharField(max_length=1, default=SUCCESS, choices=LOGIN_STATUS, null=True, blank=True)
    loginDateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.emailaddress, self.loginDateTime, self.ip)








import logging
from django.contrib.auth import user_logged_in, user_login_failed
from django.dispatch import receiver

error_log = logging.getLogger('error')


@receiver(user_logged_in)
def log_user_logged_in_success(sender, user, request, **kwargs):
    try:
        user_agent_info = request.META.get('HTTP_USER_AGENT', '<unknown>')[:255],
        user_login_activity_log = UserLoginAudit(ip=get_client_ip(request),
                                                    username=user.username,
                                                    emailaddress = user.email,
                                                    user_agent_info=user_agent_info,
                                                    status=UserLoginAudit.SUCCESS)
        user_login_activity_log.save()
    except Exception as e:
        # log the error
        error_log.error("log_user_logged_in request: %s, error: %s" % (request, e))


@receiver(user_login_failed)
def log_user_logged_in_failed(sender, credentials, request, **kwargs):
    try:
        user_agent_info = request.META.get('HTTP_USER_AGENT', '<unknown>')[:255],
        user_login_activity_log = UserLoginAudit(ip=get_client_ip(request),
                                                    emailaddress=credentials['email'],
                                                    user_agent_info=user_agent_info,
                                                    status=UserLoginAudit.FAILED)
        user_login_activity_log.save()
    except Exception as e:
        # log the error
        error_log.error("log_user_logged_in request: %s, error: %s" % (request, e))

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
