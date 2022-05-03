from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group

admin.site.site_header = "Tracking Automated Leads Admin"
admin.site.site_title = "Tracking Automated Leads Admin Portal"
admin.site.index_title = "Welcome to Tracking Automated Leads Portal"
admin.site.unregister(Group)


@admin.register(Profile)
class OriginAdmin(admin.ModelAdmin):
    list_display = ("email","first_name","last_name","company","is_active","subscription","subscription_type")
   
