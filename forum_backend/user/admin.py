from django.contrib import admin
from user.models import UserProfile,UserLog
# Register your models here.

class UserLogModelAdmin(admin.ModelAdmin):
    list_display = ['id','username','request_ip','request_path','request_type','created']
    list_display_links = ['username']
    list_filter = ['username','request_ip','request_type']
    search_fields = ['username','request_ip','request_path','request_type']
    class Meta:
        model = UserLog

admin.site.register(UserProfile)
admin.site.register(UserLog,UserLogModelAdmin)