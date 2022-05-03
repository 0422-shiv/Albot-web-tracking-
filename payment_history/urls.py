from django.urls import path
from .views import *

urlpatterns = [
  
    path('', PaymentHistoryView.as_view(), name='payment_history_view'),
    
    ]