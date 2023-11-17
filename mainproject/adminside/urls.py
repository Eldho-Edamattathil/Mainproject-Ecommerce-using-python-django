from django.contrib import admin
from django.urls import path
from adminside import views


app_name = "adminside"
urlpatterns = [
 
  path('adminlogin', views.admin_login, name ='admin_login'),
  path('adminlogout',views.admin_logout,name='admin_logout'),
  
  
  path('users_list',views.users_list,name='users_list'),
  path('block_unblock_user/<int:user_id>/',views.block_unblock_user,name='block_unblock_user')
  
  
]