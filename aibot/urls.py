"""aibot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'aibot.utils.handler404'
handler500 = 'aibot.utils.handler500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('user.urls', 'user'), namespace='user_app')),
    path('tracking-code/', include(('tracking_code.urls', 'tracking_code'), namespace='tracking_code_app')),
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard_app')),
   
    path('my-plan/', include(('my_plan.urls', 'my_plan'), namespace='my_plan_app')),
    path('payment-history/', include(('payment_history.urls', 'payment_history'), namespace='payment_history_app')),
    path('my-profile/', include(('my_profile.urls', 'my_profile'), namespace='my_profile_app')),
   
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)