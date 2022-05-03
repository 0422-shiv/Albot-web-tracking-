from django.shortcuts import render, HttpResponseRedirect,get_object_or_404,redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from braces.views import CsrfExemptMixin
from django.views import generic
from .models import MonthlyPlans,UserSubscriptionPaymentHistory,StripeKeys,ContactUs,PlanCancelRequest
import datetime
from user.models import Profile
from django.utils import timezone
import stripe
from django.contrib import messages

if StripeKeys.objects.last():
    STRIPE_PUBLISHABLE_KEY = StripeKeys.objects.last().api_key
    STRIPE_SECRET_KEY = StripeKeys.objects.last().secret_key
else:
    STRIPE_PUBLISHABLE_KEY = 'pk_test_51IkT17Eh5BgqRy5v8Wxx7nyBSIPv80TmuEtc3SybEvl8B5EFJQSoA7V3zqehPZW1xDzmqWCYRnVEiHbjQNKKHwfz00jdehacS4'
    STRIPE_SECRET_KEY = 'sk_test_51IkT17Eh5BgqRy5vhUBYMrkQsjBez07OKIwZ92sGUy4MKJmFz1Ht12b9X1n3InMjhFQiZrSBR179zamrvJr0HQt600mLYAE8P0'

# Create your views here.
@method_decorator(login_required(login_url='/'), name='dispatch')
class MyPlanView(generic.View):

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id:
            stripe.api_key = STRIPE_SECRET_KEY
            session = stripe.checkout.Session.retrieve(session_id)
            payment = get_object_or_404(UserSubscriptionPaymentHistory, stripe_payment_intent=session.payment_intent)
            payment.payment_status = True
            payment.save()
            Profile.objects.filter(id=request.user.id).update(subscription=payment.plan_id,
                subscription_start_date=datetime.datetime.now(),
                subscription_type='paid',
                subscription_expire_date=datetime.datetime.now()+datetime.timedelta(days=30)) 
            return HttpResponseRedirect(reverse('my_plan_app:my_plan_view'))
        get_plans=MonthlyPlans.objects.all()        
        return render (request, 'my_plan/my-plan.html',{"get_plans":get_plans,"current_date_time":timezone.now()})


@method_decorator(login_required(login_url='/'), name='dispatch')
class UpgradePlanView(CsrfExemptMixin, generic.View):

    def get(self, request,pk, *args, **kwargs): 
        plan=MonthlyPlans.objects.get(id=pk)
        amount=float(plan.per_month_charge_in_pound)
     
        if plan.is_trial_plan and request.user.subscription == None :
            current_user=request.user
            current_user.subscription=plan
            current_user.subscription_type='free'
            current_user.subscription_expire_date=datetime.datetime.now()+datetime.timedelta(days=plan.no_of_trial_days)
            current_user.save()
            return HttpResponseRedirect(reverse('my_plan_app:my_plan_view'))
        else:
            stripe.api_key = STRIPE_SECRET_KEY
            checkout_session = stripe.checkout.Session.create(
                customer_email = request.user.email,
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'gbp',
                            'product_data': {
                            'name':'Plan '+ plan.plan,
                            },
                            'unit_amount': int((amount)*100),
                        },
                        'quantity': 1,
                    }
                ],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('my_plan:my_plan_view') ) + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=request.build_absolute_uri(reverse('my_plan:my_plan_view')),
            ) 

            UserSubscriptionPaymentHistory.objects.create(user_id=request.user,plan_id=plan,
                                                            amount=plan.per_month_charge_in_pound,
                                                            payment_method=checkout_session["payment_method_types"][0],
                                                            created_by=request.user,
                                                            stripe_payment_intent=checkout_session["payment_intent"]) 
            return redirect(checkout_session["url"])

@method_decorator(login_required(login_url='/'), name='dispatch')
class PlanCancelView(generic.View):

    def post(self, request, *args, **kwargs): 
        
        email=request.POST.get('email')
        message = request.POST.get('message')
        cancel_request = PlanCancelRequest(email=email,message=message,created_by=request.user,update_by=request.user)
        cancel_request.save()
        messages.success(request, 'Cancellation request has been sent successfully')
        return HttpResponseRedirect(reverse('my_plan_app:my_plan_view'))
    
@method_decorator(login_required(login_url='/'), name='dispatch')
class ContactUsView(generic.View):
    
    def get(self, request, *args, **kwargs): 
        return render(request, 'my_plan/contact-us.html',{"contact_us":"Contact Us"})
    
    def post(self, request, *args, **kwargs): 
        name=request.POST.get('name')
        email=request.POST.get('email')
        message = request.POST.get('message')
        contact = ContactUs(name=name,email=email,message=message,created_by=request.user,update_by=request.user)
        contact.save()
        messages.success(request, 'Request send successfully')
        return HttpResponseRedirect(reverse('my_plan_app:my_plan_view'))
        
    #Testing card number
    
#     NUMBER         BRAND                            CVC   
# 4242424242424242	Visa	                    Any 3 digits	
# 4000056655665556	Visa (debit)	            Any 3 digits	
# 5555555555554444	Mastercard	                Any 3 digits	
# 2223003122003222	Mastercard (2-series)	    Any 3 digits	
# 5105105105105100	Mastercard (prepaid)	    Any 3 digits	
# 378282246310005	    American Express	         Any 4 digits
# 371449635398431	    American Express	        Any 4 digits
# 6011111111111117	Discover	                Any 3 digits	
# 6011000990139424	Discover	                Any 3 digits	
# 3056930009020004	Diners Club	                Any 3 digits	
# 36227206271667	     Diners Club(14 digit card) Any 3 digits	
# 3566002020360505	JCB	                       Any 3 digits	
# 6200000000000005	UnionPay	                Any 3 digits	

