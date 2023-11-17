from django.contrib import admin
from django.urls import path
from userauths import views

app_name = "userauths"


urlpatterns = [
  path('sign-up/', views.register_view, name='signup'),
  path('login/', views.login_view, name='login'),
  path('logout/', views.logoutUser, name='logout'),
  path('sign-up/otp_verification',views.otp_verification,name="otp_verification")
  

]