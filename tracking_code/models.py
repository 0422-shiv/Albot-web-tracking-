from django.db import models
from user.models import Profile
from custom.basemodel import BaseModel
import uuid

# Create your models here.
class TrackingCode(BaseModel):

    company_name = models.CharField(max_length=255, blank=True, null=True)
    web_page_name = models.CharField(max_length=255, blank=True, null=True)
    script_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status=models.BooleanField(default=True)

    class Meta:
        db_table = 'tracking_code'

    def __str__(self):
        return str(self.company_name)

class VisitorsLog(BaseModel):

    ip_address = models.GenericIPAddressField(blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    browser = models.CharField(max_length=255, blank=True, null=True)
    visitors = models.BigIntegerField(blank=True, null=True)
    web_page_url=models.URLField(null=True,blank=True)
    company_name= models.CharField(max_length=255, blank=True, null=True)
    time_on_page = models.BigIntegerField(default=0 ,blank=True, null=True)
    tracking_code_id = models.ForeignKey(TrackingCode, null=True, blank=True,
        on_delete=models.CASCADE)
    device_id = models.JSONField(verbose_name="device id", null=True)

    class Meta:
        db_table = 'visitors_log'

    def __str__(self):
        return str(self.ip_address)