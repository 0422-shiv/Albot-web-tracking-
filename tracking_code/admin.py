from django.contrib import admin
from .models import TrackingCode,VisitorsLog
from django.contrib.admin.options import ModelAdmin

# Register your models here.
class TrackingCodeAdmin(ModelAdmin):
    list_display = ["company_name","web_page_name","script_id","created_at","created_by","update_at","update_by"]
admin.site.register(TrackingCode,TrackingCodeAdmin)

@admin.register(VisitorsLog)
class VisitorsLogAdmin(admin.ModelAdmin):
    list_display = ["web_page_url","ip_address","country","browser","visitors","time_on_page","tracking_code_id"]
    list_per_page = 250
