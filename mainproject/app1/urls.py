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
  
  path('filter-products/', views.filter_product,name='filter-product'),
  # ajax for vaiants
  # path('get-variant-details/<str:product_id>/<str:variant_size>/', views.get_variant_details, name='get_variant_details'),

  # add to cart
  path('add-to-cart/', views.add_to_cart, name = 'add-to-cart'),
  
  #cart view
  path('cart/',views.cart_view,name ="cart"),
  
  path('delete-from-cart/', views.delete_item_from_cart, name="delete-from-cart"),
  
  
  # update from cart
  path('update-cart/', views.update_from_cart, name ="update-cart"),
  
  
  #checkout
  
  path('checkout/',views.checkout_view,name= 'checkout')
]