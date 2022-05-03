from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.views import generic
from django.contrib.auth.hashers import make_password, check_password
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from user.models import Profile
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Create your views here.

@method_decorator(login_required(login_url='/'), name='dispatch')
class MyProfileView(generic.View):

    def get(self, request, *args, **kwargs):
        return render (request, 'my_profile/my-profile.html')

    def post(self, request, *args, **kwargs):
        editprofile = request.POST['editprofile']
        if 'manage_profile' == editprofile:
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            company = request.POST['company']
            Profile.objects.filter(email=email).update(first_name=first_name, last_name=last_name,
                company=company)
            messages.success(request, "Profile updated successfully")
            return HttpResponseRedirect(reverse('my_profile_app:my_profile_view'))

        elif 'upload_image' == editprofile:
            email = request.POST['email']
            user_instance = get_object_or_404(Profile, email=email.lower())
            user_instance.profile_image = request.FILES['profile_image']
            user_instance.save()
            messages.success(request, "Profile Image updated successfully")
            return redirect('my_profile_app:my_profile_view')

        else:
            email = request.POST['email']
            user_instance = get_object_or_404(Profile, email=email.lower())
            if user_instance.check_password(request.POST["old_password"]):
                password1 = request.POST["password1"]
                password2 = request.POST["password2"]
                if password1 == password2:
                    user_instance.set_password(password2)
                    user_instance.save()
                    user = authenticate(email=email, password=password2) #<-- here!!
                    if user is not None:
                        login(request,user)
                        messages.success(request, "Password changed successfully")
                        return redirect('my_profile_app:my_profile_view')
                    else:
                        return redirect('user_app:login_view')
                else:
                    messages.error(request, "New Password and Confirm Password didn't match")
                    return redirect('my_profile_app:my_profile_view')
            else:
                messages.error(request, "Please Enter Correct Old Password")
                return HttpResponseRedirect(reverse('my_profile_app:my_profile_view'))
