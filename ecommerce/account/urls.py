
from django.urls import path
# we are using django's built in  password reset view
from django.contrib.auth import views as auth_views

from . import views



urlpatterns = [
   # registration urls
   path("register", views.register, name="register"),
   path("email-verification/<str:uidb64>/<str:token>/", views.email_verification, name="email_verification"), # uidb64=userid
   path("email-verification-sent", views.email_verification_sent, name="email_verification_sent"),
   path("email-verification-success", views.email_verification_success, name="email_verification_success"),
   path("email-verification-fail", views.email_verification_fail, name="email_verification_fail"),

   # login/logout urls
   path("login", views.login, name="login"),
   path("logout", views.logout, name="logout"),

   # profile / dashboard urls
   path('dashboard', views.dashboard, name='dashboard'),
   path('profile_management', views.profile_management, name='profile_management'),
   path('delete_account', views.delete_account, name='delete_account'),

   # password management urls/views
   # form to enter email to which password reset link in sent
   path('reset_password', 
        auth_views.PasswordResetView.as_view(
            template_name='account/password/password-reset.html'
            ), 
        name='reset_password'),
   
   # success mssg stating password reset email is sent
   path('reset_password_sent', 
        auth_views.PasswordResetDoneView.as_view(
         template_name='account/password/password-reset-sent.html'
        ), 
        name='password_reset_done'),
   
   # password reset link is sent to our email, by clicking that link u enter new password
   path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
         template_name='account/password/password-reset-form.html'  
        ), 
        name='password_reset_confirm'),
   
   # success mssg stating password was reset
   path('reset_password_complete', 
        auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password/password-reset-complete.html'
        ), 
        name='password_reset_complete'),
   
   # shipping/payment urls
   path('shipping', views.manage_shipping, name='shipping'),

   # track orders url
   path('track_orders', views.track_orders, name='track_orders'),

]
