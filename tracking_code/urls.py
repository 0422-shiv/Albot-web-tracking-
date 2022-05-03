from django.urls import path
from .views import *

urlpatterns = [
    #Tracking code
    path('', Tracking, name='tracking_code'),
    # path('view/', TrackingCodeView.as_view(), name='tracking_code_view'),
    path('generate-tracking-code/', GenerateTrackingCodeView.as_view(), name='generate_tracking_code_view'),
    path('user-tracking-code/', UserTrackingCodeView.as_view(), name='user_tracking_code_view'),
    path('user-tracking-code-details/<str:script_id>/', UserTrackingCodeDetailView.as_view(), name='user_tracking_code_detail_view'),
    path('update-user-tracking-code-details/<str:script_id>/', UpdateUserTrackingCodeDetailView.as_view(), name='update_user_tracking_code_detail_view'),
    path('update-user-tracking-code-status/', UpdateUserTrackingCodeStatus.as_view(), name='update_user_tracking_code_status'),
    path('delete-user-tracking-code/', DeleteUserTrackingCodeView.as_view(), name='delete_user_tracking_code_view'),
   
    path('visitors-log/', VisitorsLogView.as_view(), name='visitors_log_view'),
    path('delete-visitor-log/', DeleteVisitorLogView.as_view(), name='delete_visitor_log_view'),
    
    path('export-data/', ExportOrders, name='export_visitors_log_data'),
    ]