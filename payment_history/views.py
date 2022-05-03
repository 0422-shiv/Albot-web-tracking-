from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from braces.views import CsrfExemptMixin
from django.views import generic
from my_plan.models import UserSubscriptionPaymentHistory
# Create your views here.
@method_decorator(login_required(login_url='/'), name='dispatch')
class PaymentHistoryView(CsrfExemptMixin, generic.View):

    def get(self, request, *args, **kwargs):
        get_payment_history=UserSubscriptionPaymentHistory.objects.filter(user_id=request.user).order_by('-id')
        return render (request, 'payment_history/payment-history.html',{"get_payment_history":get_payment_history})