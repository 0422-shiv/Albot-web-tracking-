import email
from django.db import models
from custom.basemodel import BaseModel
from aibot import settings
# Create your models here.
class MonthlyPlans(models.Model):
    plan=models.CharField(max_length=20)
    is_trial_plan=models.BooleanField(default=False)
    no_of_trial_days = models.IntegerField(null=True,blank=True)
    per_month_charge_in_dollar=models.CharField(max_length=20)
    per_month_charge_in_pound=models.CharField(max_length=20,null=True,blank=True)
    linkedin_warm_up=models.BooleanField(default=False)
    email_warm_up=models.BooleanField(default=False)
    daily_email_limit=models.CharField(max_length=20)
    weekly_connection_limit=models.CharField(max_length=20)
    email_enrichment=models.BooleanField(default=False)
    linkedin_messages_free=models.CharField(max_length=20)
    linkedin_messages_paid=models.CharField(max_length=20)
    linkedIn_inmail_paid=models.CharField(max_length=20)
    one_two_one_marketing=models.BooleanField(default=False)
    view_prospects_profile=models.BooleanField(default=False)
    like_prospect_recent_post=models.BooleanField(default=False)
    endorse_linkedin_profile=models.BooleanField(default=False)
    crm_Management=models.BooleanField(default=False)
    crm_export=models.BooleanField(default=False)
    social_content=models.BooleanField(default=False)
    profile_views=models.BooleanField(default=False)
    ssi_seo=models.BooleanField(default=False)
    score_inbox_management=models.BooleanField(default=False)
    no_of_companies_to_identify=models.IntegerField(default=0)
    no_of_website=models.IntegerField(default=1)
    no_of_tracking_code=models.IntegerField(default=1)
    
    class Meta:
        verbose_name = 'Monthly Plan'
        verbose_name_plural = 'Monthly Plans'
    
    def __str__(self) -> str:
        return self.plan
    
class StripeKeys(BaseModel,models.Model): 
    api_key= models.CharField(max_length=255)
    secret_key= models.CharField(max_length=255)
    
    class Meta:
        verbose_name = 'Stripe Key'
        verbose_name_plural = 'Stripe Keys'
    
    def __str__(self) -> str:
        return self.api_key

class UserSubscriptionPaymentHistory(BaseModel,models.Model):
    user_id=models.ForeignKey(settings.AUTH_USER_MODEL,related_name="user_subscription", on_delete=models.CASCADE)
    plan_id=models.ForeignKey(MonthlyPlans,related_name="subscription_plan", on_delete=models.CASCADE)
    payment_status=models.BooleanField(default=False)
    amount=models.FloatField(null=True,blank=True)
    payment_method=models.CharField(max_length=20,null=True,blank=True)
    stripe_payment_intent = models.CharField(max_length=255,null=True,blank=True)

    class Meta:
        verbose_name = 'User subscription payment history'
        verbose_name_plural = 'User subscription payment history'
    
    def __str__(self) -> str:
            return self.user_id.email

class PlanCancelRequest(BaseModel,models.Model):
   
    email= models.EmailField(null=True,blank=True)
    message = models.TextField(null=True,blank=True)

    def __str__(self) -> str:
            return self.email


      
class ContactUs(BaseModel,models.Model):
    name=models.CharField(max_length=20,null=True,blank=True)
    email= models.EmailField(null=True,blank=True)
    message = models.TextField(null=True,blank=True)

    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'
    
    def __str__(self) -> str:
            return self.name
    
    
    
