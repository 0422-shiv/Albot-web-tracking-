from django.urls import path
from .views import *

urlpatterns = [
   
    path('', OverviewView.as_view(), name='overview_view'),
  
    ]