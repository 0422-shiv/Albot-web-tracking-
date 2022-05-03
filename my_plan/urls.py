from django.urls import path
from .views import *

urlpatterns = [
  
    path('', MyPlanView.as_view(), name='my_plan_view'),
    path('upgrade-plan/<int:pk>', UpgradePlanView.as_view(), name='upgrade_plan_view'),
    path('plan-cancel/', PlanCancelView.as_view(), name='plan_cancel_view'),
    path('contact-us/', ContactUsView.as_view(), name='contact_us_view'),
    
    ]