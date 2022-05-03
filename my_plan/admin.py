from django.contrib import admin
from.models import MonthlyPlans,StripeKeys,UserSubscriptionPaymentHistory,ContactUs,PlanCancelRequest
# Register your models here.

admin.site.register(StripeKeys)


@admin.register(UserSubscriptionPaymentHistory)
class OriginAdmin(admin.ModelAdmin):
    list_display = ("user_id","plan_id","payment_status","amount","payment_method","stripe_payment_intent")
    
@admin.register(PlanCancelRequest)
class OriginAdmin(admin.ModelAdmin):
    list_display = ("email","message")
    
# @admin.register(ContactUs)
# class OriginAdmin(admin.ModelAdmin):
#     list_display = ("name","email","message")
    
@admin.register(MonthlyPlans)
class OriginAdmin(admin.ModelAdmin):
    list_display = ("plan","is_trial_plan","no_of_trial_days","per_month_charge_in_pound","no_of_website","no_of_tracking_code","no_of_companies_to_identify")
    
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False