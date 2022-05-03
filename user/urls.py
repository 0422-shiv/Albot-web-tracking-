from django.urls import path
from .views import LoginView,RegisterView,LogoutView,SubscribeView,PasswordResetView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
urlpatterns = [
    path('', LoginView.as_view(), name='login_view'),
    path('register/<int:pk>', RegisterView.as_view(), name='register_view'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe_view'),
    path('logout/', LogoutView.as_view(), name='logout_view'),

    # Forget Password
    path('password-reset/',   PasswordResetView.as_view(success_url = reverse_lazy('user_app:password_reset_done')),name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='user/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='user/password-reset/password_reset_confirm.html',
             success_url =  reverse_lazy('user_app:password_reset_complete')
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='user/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    ]