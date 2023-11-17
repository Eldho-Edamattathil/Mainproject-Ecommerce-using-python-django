from django.urls import path
from admindash import views


app_name='admindash'

urlpatterns = [
    path('dashboard',views.dashboard,name='dashboard'),
    path('admin_products_list',views.admin_products_list,name='admin_products_list'),
    path('admin_products_details/<pid>/',views.admin_products_details,name='admin_products_details'),
]