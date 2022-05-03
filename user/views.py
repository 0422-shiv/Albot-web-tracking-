from datetime import timedelta
from django.views import generic
from .forms import *
from .models import *
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, redirect,get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from my_plan.models import MonthlyPlans
import datetime
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from braces.views import CsrfExemptMixin
from my_plan.models import UserSubscriptionPaymentHistory,StripeKeys
import stripe


if StripeKeys.objects.last():
    STRIPE_PUBLISHABLE_KEY = StripeKeys.objects.last().api_key
    STRIPE_SECRET_KEY = StripeKeys.objects.last().secret_key
else:
    STRIPE_PUBLISHABLE_KEY = 'pk_test_51IkT17Eh5BgqRy5v8Wxx7nyBSIPv80TmuEtc3SybEvl8B5EFJQSoA7V3zqehPZW1xDzmqWCYRnVEiHbjQNKKHwfz00jdehacS4'
    STRIPE_SECRET_KEY = 'sk_test_51IkT17Eh5BgqRy5vhUBYMrkQsjBez07OKIwZ92sGUy4MKJmFz1Ht12b9X1n3InMjhFQiZrSBR179zamrvJr0HQt600mLYAE8P0'


class LoginView(CsrfExemptMixin,generic.View):

    def get(self, request, *args, **kwargs):
        log_in_form = LoginForm
        session_id = request.GET.get('session_id')
        user = request.GET.get('user')
       
        if session_id and user:
            stripe.api_key = STRIPE_SECRET_KEY
            session = stripe.checkout.Session.retrieve(session_id)
            payment = get_object_or_404(UserSubscriptionPaymentHistory, stripe_payment_intent=session.payment_intent)
            payment.payment_status = True
            payment.save()
            
            Profile.objects.filter(email=user).update(subscription=payment.plan_id,
                subscription_start_date=datetime.datetime.now(),
                subscription_type='paid',
                subscription_expire_date=datetime.datetime.now()+datetime.timedelta(days=30)) 
            user=Profile.objects.get(email=user)
            if user is not None:
                login(request,user)
           
            messages.success(request, 'Registration Successful')
            
            return redirect('dashboard_app:overview_view')
       
        return render (request, 'user/login.html', {'log_in_form':log_in_form})

    def post(self, request, *args, **kwargs):
        logout(request)
        email = password = ''
        log_in_form = LoginForm(request.POST)
        email = request.POST['email']
        password = request.POST['password1']
        if Profile.objects.filter(email=email).exists():
            user = authenticate(request, email = email, password = password)
            if user is not None:
                login(request, user)
                messages.success(request, f' Welcome {user.first_name}!')
                return redirect('dashboard_app:overview_view')
            else:
                messages.error(request, "Please enter Correct Password")
                return redirect('user_app:login_view')
        else:
            messages.error(request, "This Email doesn't exists, Please enter Correct Email or Register")
            return HttpResponseRedirect(reverse('user_app:login_view'))

class LogoutView(generic.View):

    def get(self, request):
        logout(request)
        messages.success(request, 'You logged out Successfully')
        return redirect('user_app:login_view')

class SubscribeView(generic.View):
        def get(self, request, *args, **kwargs):
            get_plans=MonthlyPlans.objects.all().order_by('id')
            return render (request, 'user/subscription.html',{"get_plans":get_plans})

class RegisterView(generic.View):

    def get(self, request,pk, *args, **kwargs):
        register_form = RegisterForm
        plan=MonthlyPlans.objects.get(id=pk)
        user = authenticate(email='admin@gmail.com', password=123) 
        print(user)
        return render (request, 'user/register.html' , {'register_form':register_form,"id":pk,"plan":plan})

    def post(self, request,pk, *args, **kwargs):
        register_form = RegisterForm(request.POST)
        email = request.POST['email']
        password1 = request.POST["password1"]
        if Profile.objects.filter(email=email).exists():
            messages.error(request, 'Entered Email already exits')
            return redirect("/register/"+str(pk))
        else:
            if register_form.is_valid():
                register_form.save()
                user = authenticate(email=email, password=password1) 
                plan=MonthlyPlans.objects.get(id=pk)
                if plan.is_trial_plan:
                    if user is not None:
                        login(request,user)
                        current_user=request.user
                    current_user.subscription=plan
                    current_user.subscription_type='free'
                    current_user.subscription_expire_date=datetime.datetime.now()+timedelta(days=plan.no_of_trial_days)
                    current_user.save()
                    # importing the requests library
                    import requests

                    # api-endpoint
                    URL = "https://api.vbout.com/1/emailmarketing/addcontact.json?key=8085507234778445078830662"

                    # location given here
                    email=request.user.email
                    status="active"
                    listid=65017
                
                    # defining a params dict for the parameters to be sent to the API
                    PARAMS = {'email':email,'status':status,'listid':listid,'fields[495384]':request.user.first_name ,
                            'fields[495385]':request.user.last_name}#'fields[495387]'for phone number

                    # sending get request and saving the response as response object
                    r = requests.post(url = URL, params = PARAMS)

                    # extracting data in json format
                    # data = r.json()
                    messages.success(request, 'Registration Successful')
                    return redirect('dashboard_app:overview_view')
                else:
                    stripe.api_key = STRIPE_SECRET_KEY
                    checkout_session = stripe.checkout.Session.create(
                        customer_email = email,
                        payment_method_types=['card'],
                        line_items=[
                            {
                                'price_data': {
                                    'currency': 'gbp',
                                    'product_data': {
                                    'name': plan.plan,
                                    },
                                    'unit_amount': int(float(plan.per_month_charge_in_pound)*100),
                                },
                                'quantity': 1,
                            }
                        ],
                        mode='payment',
                        success_url=request.build_absolute_uri(reverse('user_app:login_view') ) + "?session_id={CHECKOUT_SESSION_ID}&user="+str(user),
                        cancel_url=request.build_absolute_uri(reverse('user_app:register_view', kwargs={'pk': plan.id} )),
                    ) 
                    user_instance=Profile.objects.get(email=email)
                    UserSubscriptionPaymentHistory.objects.create(user_id=user_instance,plan_id=plan,
                                                                    amount=plan.per_month_charge_in_pound,
                                                                    payment_method=checkout_session["payment_method_types"][0],
                                                                    created_by=user_instance,
                                                                    stripe_payment_intent=checkout_session["payment_intent"]) 
                    return redirect(checkout_session["url"])
                        # current_user.subscription=plan
                        # current_user.subscription_type='free'
                        # current_user.subscription_expire_date=datetime.datetime.now()+timedelta(days=plan.no_of_trial_days)
                        # current_user.save()
                        # messages.success(request, 'Registration Successful')
                        # return redirect('dashboard_app:overview_view')
            else:
                messages.error(request, register_form.errors)
                return redirect("/register/"+str(pk))


class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context


class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = 'user/password-reset/password_reset_email.html',
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = settings.DEFAULT_FROM_EMAIL
    html_email_template_name = None
    subject_template_name = 'user/password-reset/password_reset_subject.txt'
    success_url = reverse_lazy('password.reset.done')
    template_name ='user/password-reset/password_reset.html'
    title = _('Password reset')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)
    
