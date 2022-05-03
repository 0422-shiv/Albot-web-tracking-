from django.urls import path
from .views import *

urlpatterns = [
    path('', MyProfileView.as_view(), name='my_profile_view'),
    ]