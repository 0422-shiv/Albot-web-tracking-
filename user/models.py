from ast import Subscript
from django.db import models
import uuid
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from custom.basemodel import BaseModel
from django_resized import ResizedImageField
from my_plan.models import MonthlyPlans

class ProfileManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if email is None:
            raise ValueError('Users should have a Email')
        if password is None:
            raise ValueError('Password should not be none')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if email is None:
            raise ValueError('Users should have a Email')
        if password is None:
            raise ValueError('Password should not be none')

        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class Profile(AbstractBaseUser, PermissionsMixin,BaseModel):
    
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    accept = models.BooleanField(default=False,null=False)
    profile_image = models.ImageField(default='default_profile_image.jpg',
        upload_to='Profile_Images/%Y/%m/%d',blank=True, null=True)
    subscription = models.ForeignKey(MonthlyPlans, related_name="user_subscription_plan", verbose_name="subscription plan", on_delete=models.CASCADE,null=True,blank=True)
    subscription_type=models.CharField(max_length=10,null=True,blank=True) # type will free or paid
    subscription_start_date= models.DateTimeField(auto_now=True, null=True, blank=True)
    subscription_expire_date= models.DateTimeField(null=True, blank=True)
    USERNAME_FIELD = 'email'

    objects = ProfileManager()

    def __str__(self):
        return self.email

