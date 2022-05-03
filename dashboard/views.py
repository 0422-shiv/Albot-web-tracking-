from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
from django.urls import reverse
from django.views import generic
from user.models import *
from tracking_code.models import VisitorsLog,TrackingCode
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.defaulttags import register
from statistics import mean 
import datetime as dt
from collections import Counter
from django.utils import timezone

today = dt.date.today()



@method_decorator(login_required(login_url='/'), name='dispatch')
class OverviewView(generic.View):

    def get(self, request, *args, **kwargs):
                  
        if not request.user.subscription == None:  
            
            query=VisitorsLog.objects.filter(
                tracking_code_id__in=TrackingCode.objects.filter(created_by=request.user))
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
            
            #filter by days
            if request.GET.get("sort_by_days"):
                query = query.filter(created_at__gte=dt.datetime.now()-dt.timedelta(days=int(request.GET.get("sort_by_days"))))
            
            #filter by current month
            if request.GET.get("sort_by_month"):
                query = query.filter(created_at__month=today.month)
            
            #filter by current year
            if request.GET.get("sort_by_year"):
                query = query.filter(created_at__year=today.year)
            
            
            # get latest companies visits
            latest_companies= query.values_list("company_name",flat=True) .order_by('company_name', '-id').distinct("company_name")
            
            
            # get top country    
            country_users=query.values_list("country",flat=True).distinct("country")
            total_country_users=country_users.count()
            if not total_country_users % 2 == 0:
                total_country_users=total_country_users+1
            first_half_country_users=country_users[:total_country_users/2]
            second_half_country_users=country_users[total_country_users/2:]
            
            # get top browser
            brower_list=[]
            for data in query.values_list("browser",flat=True):
                brower_list.append(data)
            top_browser=most_frequent_browser(brower_list)
            
            # get average time 
            average =query.values_list('time_on_page', flat=True)
            a_l = []
            for a in average:
                a_l.append(a)
            if a_l:
                avg = round(mean(a_l))
            else:
                avg=0
            avg_time = str(dt.timedelta(seconds = avg))
            
            
            #get top visited pages
            top_visited_pages=[]
            for data in query.order_by("-visitors")[0:10]:
                top_visited_pages.append(data.web_page_url)
                # print(data.web_page_url)
            # top_visited_pages_list=[]
            # for data in query.values_list("web_page_url","visitors",flat=True):
            #     top_visited_pages_list.append(data)
            # top_visited_pages=most_frequent_urls(top_visited_pages_list)
            
            #total visitors
            total_visitors =  []
            
            for data in query:
                for item in data.device_id:
                    if not item in  total_visitors:
                        total_visitors.append(item)   
            total_visitors=len(total_visitors)

            context={'latest_companies':latest_companies,
                    'first_half_country_users':first_half_country_users,
                    'second_half_country_users':second_half_country_users,
                    # 'total_visitors':query.distinct("ip_address").count(),
                    'total_visitors':total_visitors,
                    'top_browser':top_browser,
                    'avg_time':avg_time,
                    'top_visited_pages':top_visited_pages,
                    'sort_by':request.GET.get("sort_by_days") or request.GET.get("sort_by_month") or request.GET.get("sort_by_year"),
                    }
            return render (request, 'dashboard/overview-dashboard.html',context)
        else:
            return HttpResponseRedirect(reverse('my_plan_app:my_plan_view'))  


@register.simple_tag(takes_context = True)
def get_country_users(context,country_name,sort_by):
    request = context['request']
    query=VisitorsLog.objects.filter(tracking_code_id__in=TrackingCode.objects.filter(created_by=request.user)).filter(country=country_name)
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
    total_visitors =  []
    

    #filter by current year
    if sort_by == "current_year":
        query = query.filter(created_at__year=today.year)
    
    #filter by current month
    if sort_by == "current_month" :
        query = query.filter(created_at__month=today.month)
    
    #filter by days
    if sort_by:
        if not sort_by == "current_month" and not sort_by == "current_year":
            query=query.filter(created_at__gte=timezone.now()-dt.timedelta(days=int(sort_by)))
    for data in query:
        for item in data.device_id:
            if not item in  total_visitors:
                total_visitors.append(item)   
    total_visitors=len(total_visitors)
    return total_visitors

@register.simple_tag(takes_context = True)
def get_country_users_percent(context,country_name,sort_by):
    request = context['request']
    # total_users=VisitorsLog.objects.filter(tracking_code_id__in=TrackingCode.objects.filter(created_by=request.user)).distinct("ip_address").count()
    # query=VisitorsLog.objects.filter(tracking_code_id__in=TrackingCode.objects.filter(created_by=request.user)).filter(country=country_name).distinct("ip_address")
    total_users=VisitorsLog.objects.filter(tracking_code_id__in=TrackingCode.objects.filter(created_by=request.user))
    query=VisitorsLog.objects.filter(tracking_code_id__in=TrackingCode.objects.filter(created_by=request.user)).filter(country=country_name)
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
    #filter by current year
    if sort_by == "current_year":
        query = query.filter(created_at__year=today.year)
    
    #filter by current month
    if sort_by == "current_month" :
        query = query.filter(created_at__month=today.month)
    
    #filter by days
    if sort_by:
        if not sort_by == "current_month" and not sort_by == "current_year":
            query=query.filter(created_at__gte=timezone.now()-dt.timedelta(days=int(sort_by)))
    
    visitors_by_country =  []
    for data in query:
        for item in data.device_id:
            if not item in  visitors_by_country:
                visitors_by_country.append(item)   
    visitors_by_country=len(visitors_by_country)
    
    total_users_list =  []
    for data in total_users:
        for item in data.device_id:
            if not item in  total_users_list:
                total_users_list.append(item)   
    total_users_list=len(total_users_list)
    
    percent=visitors_by_country/total_users_list*100
    
    return int(percent)

def most_frequent_browser(List):
    counter = 0
    num=''
    if List:
        num = List[0]
    for i in List:
        curr_frequency = List.count('Chrome')
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
 
    return num


def most_frequent_urls(list):
    result_list=[]
    # Convert given list into dictionary
    # it's output will be like {'ccc':1,'aaa':3,'bbb':2}
    dict = Counter(list)
    # Get the list of all values and sort it in ascending order
    value = sorted(dict.values(), reverse=True)
 
        
    if len(value) > 5:
        # Pick first largest element
        firstLarge = value[0]
        # Pick second largest element
        secondLarge = value[1]
        # Pick second largest element
        ThirdLarge = value[2]
        # Pick second largest element
        fourthLarge = value[3]
        # Pick second largest element
        fifthLarge = value[4]
        # print(firstLarge,secondLarge,ThirdLarge,fourthLarge,fifthLarge)
  
    # Traverse dictionary and print key whose
    # value is equal to  large element
        for (key, val) in dict.items():
            if val == firstLarge and not key in result_list:
                 result_list.append(key)
            if val == secondLarge and not key in result_list:
                    result_list.append(key)
            if val == ThirdLarge and not key in result_list:
                    result_list.append(key)
            if val == fourthLarge and not key in result_list:
                    result_list.append(key)
            if val == fifthLarge and not key in result_list:
                    result_list.append(key)
    return result_list
                    