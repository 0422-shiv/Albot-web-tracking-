from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from braces.views import CsrfExemptMixin
from django.views import generic
from .models import *
from statistics import mean 
import datetime as dt
from aibot.settings import BASE_URL
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import xlwt
from django.core.paginator import Paginator
from django.db.models import Q
import requests
import json
from django.utils import timezone
from my_plan.models import UserSubscriptionPaymentHistory
from collections import Counter
from django.template.defaulttags import register


today = dt.date.today()
# Create your views here.

@csrf_exempt
def Tracking(request):
    try:
      device_id=request.POST['device']
      browser = request.POST['b']
      ip = request.POST['i'][1:-1] 
      web_page_url = request.POST['w']
      time = int(float(request.POST['t']))
      script_id = request.POST['s']
      
      if TrackingCode.objects.filter(status=True).filter(script_id=script_id).exists():
      
        # for data in TrackingCode.objects.filter(status=True).filter(script_id=script_id):
        #       user=data.created_by
        #       break
        
        # if user.subscription_expire_date < timezone.now():
        #     return JsonResponse({'status': 1}) 
        
        # if user.subscription.no_of_companies_to_identify <= VisitorsLog.objects.filter(tracking_code_id__script_id=script_id).filter(ip_address=ip).count():
        #     return JsonResponse({'status': 1}) 
        
        if VisitorsLog.objects.filter(tracking_code_id__script_id=script_id).filter(ip_address=ip).filter(browser=browser).filter(web_page_url=web_page_url).exists():
            visitor_instance=get_object_or_404(VisitorsLog,tracking_code_id__script_id=script_id,ip_address=ip,browser=browser,web_page_url=web_page_url)
            final_time = visitor_instance.time_on_page + time
            
            devices=visitor_instance.device_id
            if device_id in devices:
                duration_in_milliseconds = (timezone.now().replace(tzinfo=None)-dt.datetime.strptime(devices[device_id], '%Y-%m-%d %H:%M:%S.%f+00:00')).total_seconds() * 1000 
               
                if duration_in_milliseconds >= 86400000 :#86400000(24 hours)
                 
                  devices[device_id]=str(timezone.now()) 
                  VisitorsLog.objects.filter(tracking_code_id__script_id=script_id).filter(
                        ip_address=ip).filter(browser=browser).filter(web_page_url=web_page_url).update(
                          time_on_page=final_time,visitors=visitor_instance.visitors+1,device_id=devices)
            
                else:  
                    VisitorsLog.objects.filter(tracking_code_id__script_id=script_id).filter(ip_address=ip).filter(browser=browser).filter(web_page_url=web_page_url).update(time_on_page=final_time)
          
            else:
                devices[device_id]=str(timezone.now()) 
                visitor_instance.device_id=devices
                visitor_instance.save()
                VisitorsLog.objects.filter(tracking_code_id__script_id=script_id).filter(ip_address=ip).filter(
                   browser=browser).filter(web_page_url=web_page_url).update(time_on_page=final_time,visitors=visitor_instance.visitors+1)
            
           
        else:
            url = f'https://api.ipregistry.co/{ip}?key=q6ug1pbdjt5kqa9f'
            r = requests.get(url)
            data=json.loads(r.text) 
            company_name=(data.get('company')).get('name')
            country=((data.get('location')).get('country')).get('name')
            tracking_instance=get_object_or_404(TrackingCode,script_id=script_id)
            visiter_instance = VisitorsLog(company_name=company_name,ip_address=ip, country=country,browser=browser,
                                          tracking_code_id=tracking_instance, time_on_page=time,web_page_url=web_page_url,
                                          device_id={device_id:str(timezone.now())},visitors=1)
            visiter_instance.save()

      return JsonResponse({'status': 1})
    
    except:
       return JsonResponse({'status': 0})



# Generate tracking code and save it 
@method_decorator(login_required(login_url='/'), name='dispatch')
class GenerateTrackingCodeView(CsrfExemptMixin, generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.subscription == None:
          if  request.user.subscription_expire_date <= timezone.now():
              if request.user.subscription_type == "free":
                  return render (request,  'tracking_code/free-plan-expire.html') 
             
              if request.user.subscription_type == "paid":
                  return render (request,  'tracking_code/paid-plan-expire.html') 
         
          if request.user.subscription.no_of_tracking_code <= TrackingCode.objects.filter(created_by=request.user).count():
                get_tracking_code= TrackingCode.objects.filter(created_by=self.request.user)
                return render (request,'tracking_code/user-tracking-code.html',{"get_tracking_code":get_tracking_code,'show_modal':True})
          
          script_id = uuid.uuid4()
      
          # if request.user.subscription_type == "free":
          #     if TrackingCode.objects.filter(created_by=request.user).exists():
          #         get_tracking_code= TrackingCode.objects.filter(created_by=self.request.user)
          #         return render (request,'tracking_code/user-tracking-code.html',{"get_tracking_code":get_tracking_code,'show_modal':True})

          return render (request, 'tracking_code/generate-tracking-code.html',{'script_id': script_id, 'BASE_URL': BASE_URL})
        else:
            return HttpResponseRedirect(reverse('my_plan_app:my_plan_view'))
      
    
    
    def post(self, request, *args, **kwargs):
        name = request.POST['company_name']
        web_url = request.POST['webiste_url']
        script_id = request.POST['script_id']
        tc_obj= TrackingCode(script_id=script_id, created_by=request.user, update_by=request.user,company_name=name, web_page_name=web_url)
        
        if TrackingCode.objects.filter(created_by=request.user).exists():
            if request.user.subscription_type == "free":
                plan = request.user.subscription
            else:
                payment_type = UserSubscriptionPaymentHistory.objects.filter(created_by=request.user).filter(payment_status=True).last()
                plan=payment_type.plan_id
            websites=TrackingCode.objects.filter(created_by=request.user)
           
            websites_list=[]
            
            for data in websites:
                  websites_list.append(data.web_page_name)
            res = {}

            for i in websites_list:
                res[i] = websites_list.count(i)
            
            
            if plan.id == 1:
                                        
                  if web_url in res.keys():
                      tc_obj.save()
                  else:
                       messages.error(request, "One website can't have more than two scripts") 
                       return HttpResponseRedirect(reverse('tracking_code_app:user_tracking_code_view'))
                     
            elif plan.id == 2:
                  
                  
                  if web_url in res.keys():
                      
                      if res[web_url] < 2:
                        tc_obj.save()
                      else:
                        messages.error(request, "One website can't have more than two scripts") 
                        return HttpResponseRedirect(reverse('tracking_code_app:user_tracking_code_view')) 
                  
                                   
                  elif not web_url in res.keys() and len(res) < plan.no_of_website:
                        
                        tc_obj.save()
                  else:
                       messages.error(request, "One website can't have more than two scripts") 
                       return HttpResponseRedirect(reverse('tracking_code_app:user_tracking_code_view'))
            elif plan.id == 3:
                     
                  if web_url in res.keys():
                      
                      if res[web_url] < 2:
                        tc_obj.save()
                      else:
                        messages.error(request, "One website can't have more than two scripts") 
                        return HttpResponseRedirect(reverse('tracking_code_app:user_tracking_code_view')) 
                  
                                   
                  elif not web_url in res.keys() and len(res) < plan.no_of_website:
                        
                        tc_obj.save()
                  else:
                       messages.error(request, "One website can't have more than two scripts") 
                       return HttpResponseRedirect(reverse('tracking_code_app:user_tracking_code_view'))
                                        
                  
                
            else:
                get_tracking_code= TrackingCode.objects.filter(created_by=self.request.user)
                return render (request,'tracking_code/user-tracking-code.html',{"get_tracking_code":get_tracking_code,'show_modal':True})
          
                  
           
        else:
           tc_obj.save()  
        
        messages.success(request, "Script Created Successfully")  
        return HttpResponseRedirect(reverse('tracking_code_app:user_tracking_code_view'))


##############################################################################################################

# View all Tracking codes of current user
@method_decorator(login_required(login_url='/'), name='dispatch')
class UserTrackingCodeView(generic.ListView):
      template_name='tracking_code/user-tracking-code.html'
      # context_object_name ='get_tracking_code'
      
      def get(self, request, *args, **kwargs):
          if not request.user.subscription == None:
            if  request.user.subscription_expire_date <= timezone.now():
              if request.user.subscription_type == "free":
                  return render (request,  'tracking_code/free-plan-expire.html')
            if TrackingCode.objects.filter(created_by=self.request.user).exists(): 
              get_tracking_code= TrackingCode.objects.filter(created_by=self.request.user)
              return render (request,self.template_name,{"get_tracking_code":get_tracking_code})
            else:
              return render (request, 'tracking_code/tracking-code.html')  
          else:
              return HttpResponseRedirect(reverse('my_plan_app:my_plan_view'))

 
 # View Details of Tracking codes of current user 
@method_decorator(login_required(login_url='/'), name='dispatch')
class UserTrackingCodeDetailView(generic.TemplateView):
      template_name='tracking_code/user-tracking-code-details.html'
      
      def get(self, request, *args, **kwargs):
        if request.user.subscription_expire_date <= timezone.now():
            if request.user.subscription_type == "free":
              return render (request,  'tracking_code/free-plan-expire.html')
        instance=TrackingCode.objects.get(script_id=self.kwargs["script_id"])
        return render (request,self.template_name,{'instance': instance, 'BASE_URL': BASE_URL})
      
      
      
 #Update Details of Tracking codes of current user 
@method_decorator(login_required(login_url='/'), name='dispatch')
class UpdateUserTrackingCodeDetailView(CsrfExemptMixin,generic.TemplateView):
      template_name='tracking_code/update-user-tracking-code-details.html'
      
      def get(self, request, *args, **kwargs):
        if  request.user.subscription_expire_date <= timezone.now():
            if request.user.subscription_type == "free":
              return render (request,  'tracking_code/free-plan-expire.html')
        instance=TrackingCode.objects.get(script_id=self.kwargs["script_id"])
        return render (request,self.template_name,{'instance': instance, 'BASE_URL': BASE_URL})
      
      def post(self, request, *args, **kwargs):
           
        TrackingCode.objects.filter(script_id=self.kwargs["script_id"]).update(company_name=request.POST['company_name'])
        messages.success(request, "Updated Successfully")
        return HttpResponseRedirect(reverse('tracking_code_app:user_tracking_code_view'))


 #Update status of Tracking codes of current user 
@method_decorator(login_required(login_url='/'), name='dispatch')
class UpdateUserTrackingCodeStatus(CsrfExemptMixin,generic.View):
      
      def post(self, request, *args, **kwargs):
        instance=TrackingCode.objects.get(script_id=request.GET["script_id"])
        if instance.status:
            instance.status=False
        else:
             instance.status=True
        instance.save() 
        return HttpResponseRedirect(reverse('tracking_code_app:user_tracking_code_view'))


#Delete Tracking codes of current user 
@method_decorator(login_required(login_url='/'), name='dispatch')
class DeleteUserTrackingCodeView(CsrfExemptMixin,generic.View):

    def post(self, request, *args, **kwargs):
        user_instance = get_object_or_404(TrackingCode, script_id=request.GET['script_id'])
        TrackingCode.objects.filter(script_id=user_instance.script_id).delete()
        return JsonResponse({'status': 1})

###################################################################################################

@method_decorator(login_required(login_url='/'), name='dispatch')
class VisitorsLogView(generic.View):

    def get(self, request, *args, **kwargs):
        if not request.user.subscription == None:  
          if  request.user.subscription_expire_date <= timezone.now():
              if request.user.subscription_type == "free":
                return render (request,  'tracking_code/free-plan-expire.html')
          query=  VisitorsLog.objects.filter(tracking_code_id__in=TrackingCode.objects.filter(created_by=request.user))
          
          track_id=None
          if request.GET.get("tracking_id"):
            query=  query.filter(tracking_code_id=TrackingCode.objects.get(
              script_id=request.GET["tracking_id"])).filter(
                tracking_code_id__in=TrackingCode.objects.filter(created_by=request.user))
            track_id=TrackingCode.objects.get(script_id=request.GET["tracking_id"])
          
          if request.GET.get("from_date") and request.GET.get("to_date"):
              from_date = dt.datetime.strptime(request.GET.get("from_date"),"%Y-%m-%d")
              to_date = dt.datetime.strptime(request.GET.get("to_date"),"%Y-%m-%d")
              query = query.filter(created_at__range=[from_date,to_date])
          
          if request.GET.get("sort_by_days"):
              query = query.filter(created_at__gte=dt.datetime.now()-dt.timedelta(days=int(request.GET.get("sort_by_days"))))
          
          if request.GET.get("sort_by_month"):
              query = query.filter(created_at__month=today.month)
          
          if request.GET.get("sort_by_year"):
              query = query.filter(created_at__year=today.year)
          
          if request.GET.get("sort_by_personalized"):
              query = query
          
          if request.GET.get("q"):
              query = query.filter(Q(tracking_code_id__company_name__icontains=request.GET.get("q")) | Q(ip_address__icontains=request.GET.get("q")))
          
          # else:
          #   query= query.filter(tracking_code_id__in=TrackingCode.objects.filter(created_by=request.user))
          tracking_data = TrackingCode.objects.all().prefetch_related('tracking_code')
          total_visitors =  []
          
          for data in query:
              for item in data.device_id:
                   if not item in  total_visitors:
                      total_visitors.append(item)   
          total_visitors=len(total_visitors)
          average = query.values_list('time_on_page', flat=True)
          a_l = []
          for a in average:
              a_l.append(a)
          if a_l:
            avg = round(mean(a_l))
          else:
            avg=0
          avg_time = str(dt.timedelta(seconds = avg))
          browsers = query.values_list('browser', flat=True)
          adict = {'MS Edge':0, 'Edge ( chromium based)' :0,'Opera':0, 'Chrome':0, 'MS IE' :0,'Mozilla Firefox':0,
                  'Safari':0, 'other' :0}
          for browser in browsers:
              if "MS Edge" in browser:
                adict["MS Edge"] += 1
              if "Edge ( chromium based)" in browser:
                adict["Edge ( chromium based)"] += 1
              if "Opera" in browser:
                adict["Opera"] += 1
              if "Chrome" in browser:
                adict["Chrome"] += 1
              if "MS IE" in browser:
                adict["MS IE"] += 1
              if "Mozilla Firefox" in browser:
                adict["Mozilla Firefox"] += 1
              if "Safari" in browser:
                adict["Safari"] += 1
              if "other" in browser:
                adict["other"] += 1
          top_browser = max(zip(adict.values(), adict.keys()))[1]
      
          no_of_company = request.user.subscription.no_of_companies_to_identify
          data_list=[] 
          count = 1
          for data in reversed(list(query.distinct('company_name'))):
              if count  <= no_of_company:
                for item in query :
                  if data.company_name ==  item.company_name:
                     data_list.append(item)
              else:
                    break
              count+=1
        
          
          paginator = Paginator(data_list[::-1], 25) # Show 25 logs per page.
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          get_tracking_code=TrackingCode.objects.filter(created_by=request.user)
          context={
            'tracking_data': tracking_data,
            'visitors_data': page_obj, 
            'total_visitors': total_visitors,
            'avg_time': avg_time, 
            'top_browser': top_browser,
            'sort_by_days':request.GET.get("sort_by_days"),
            'sort_by_month':request.GET.get("sort_by_month"),
            'sort_by_year':request.GET.get("sort_by_year"),
            'sort_by_personalized':request.GET.get("sort_by_personalized"),
            'query':request.GET.get("q"),
            'from_date':request.GET.get("from_date") ,
            'to_date':request.GET.get("to_date"),
            'get_tracking_code':get_tracking_code,
            'track_id':track_id
            
          }
          return render (request, 'tracking_code/visitors-log.html',context)
        else:
            return HttpResponseRedirect(reverse('my_plan_app:my_plan_view'))  



# Delete Visitors logs
@method_decorator(login_required(login_url='/'), name='dispatch')
class DeleteVisitorLogView(CsrfExemptMixin, generic.View):
    
    def post(self, request, *args, **kwargs):
        id = request.GET['id']
        VisitorsLog.objects.filter(id=id).delete()
        return JsonResponse({'status': 1})
      
      
# to download visitorlog data    
@login_required(login_url='/')
def ExportOrders(request):
  response = HttpResponse(content_type='application/ms-excel')
  response['Content-Disposition'] = 'attachment; filename="visitors-data.xls"'

  wb = xlwt.Workbook(encoding='utf-8')
  ws = wb.add_sheet('Visitor log Data') # this will make a sheet named Users Data

  # Sheet header, first row
  row_num = 0

  font_style = xlwt.XFStyle()
  font_style.font.bold = True

  columns = ['Tracking Code','Company Name',"Web page name" ,'IP Address','Country','Browser','Time on page']

  for col_num in range(len(columns)):
    ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

  # Sheet body, remaining rows
  font_style = xlwt.XFStyle()
  
  query=VisitorsLog.objects.filter(tracking_code_id__in=TrackingCode.objects.filter(created_by=request.user))
  
  no_of_company = request.user.subscription.no_of_companies_to_identify
  data_list=[] 
  count = 1
  for data in reversed(list(query.distinct('company_name'))):
      if count  <= no_of_company:
        for item in query :
          if data.company_name ==  item.company_name:
              data_list.append(item.id)
      else:
            break
      count+=1
  query = query.filter(id__in=data_list)
  rows=query.values_list("tracking_code_id__company_name","company_name","web_page_url","ip_address","country","browser","time_on_page")
  for row in rows:
    row_num += 1
    for col_num in range(len(row)):
      ws.write(row_num, col_num, row[col_num], font_style)

  wb.save(response)

  return response

@register.filter(name='get_plan_upgrade')
def get_plan_upgrade(user):
    
    plan_upgrade = False
   
    query = VisitorsLog.objects.filter(tracking_code_id__in=TrackingCode.objects.filter(created_by=user))
   
    no_of_company =  user.subscription.no_of_companies_to_identify
    
    
    if no_of_company <= query.distinct('company_name').count():
        
        plan_upgrade = True
    
    return plan_upgrade       


@register.filter(name='get_tracked_ips')
def get_tracked_ips(user):
     
    query = VisitorsLog.objects.filter(tracking_code_id__in=TrackingCode.objects.filter(created_by=user))
       
    return query.distinct('company_name').count()
        
         


