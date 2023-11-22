from django.contrib import admin
from django.urls import path
from app1 import views
from app1.views import index


app_name = "app1"
urlpatterns = [
  path('', views.index, name ='index'),
  path('products/', views.product_list, name = 'product-list'),
   path('product/<pid>/', views.product_detail, name = 'product-detail'),
  
  path('category/', views.category_list, name = 'category-list'),
   path('category/<cid>/', views.category_product_list, name = 'category-product-list'),
   
   #search 
   
  path('search/',views.search_view,name='search'),
  
  #filter
  
  path('filter-products/', views.filter_product,name='filter-product')
  

  

]