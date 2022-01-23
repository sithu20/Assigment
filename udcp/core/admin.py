from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, UserOccupation, UserLoginAudit


class UserProfileInline(admin.StackedInline):
  model = UserProfile
  can_delete = False
  verbose_name_plural = 'Profile'
  fk_name = 'user'


class CustomUserAdmin(UserAdmin):
  inlines = (UserProfileInline,)


  def get_inline_instances(self, request, obj=None):
    if not obj:
      return list()
    return super(CustomUserAdmin, self).get_inline_instances(request, obj)
    

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


#UserAdmin.fieldsets += ('Custom fields set', {'fields': ('mobileno', 'memcode')}),






class UserOccupationAdmin(admin.ModelAdmin):
    list_display = ('pk','ocpName', 'ocpSalary','createBy', 'createDate')

admin.site.register(UserOccupation, UserOccupationAdmin)

class UserLoginAuditAdmin(admin.ModelAdmin):
    list_display = ('pk','username','emailaddress','status','loginDateTime')

admin.site.register(UserLoginAudit, UserLoginAuditAdmin)