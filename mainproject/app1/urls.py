from django.contrib import admin
from django.urls import path,include
from app1 import views
from app1.views import index


app_name = "app1"
urlpatterns = [
  # path('<str:ref_code>/', views.index, name='index'),
  path('', views.index, name='index'),
  path('products/', views.product_list, name = 'product-list'),
   path('product/<pid>/', views.product_detail, name = 'product-detail'),
  
  path('category/', views.category_list, name = 'category-list'),
   path('category/<cid>/', views.category_product_list, name = 'category-product-list'),
   
   path("ajax-add-review/<int:pid>/", views.add_ajax_review, name="ajax-add-review"),
   
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
  
  path('checkout/',views.checkout_view,name= 'checkout'),
  
  # dashboard
  
  path('dashboard/',views.customer_dashboard,name= 'dashboard'),
  
  path('dashboard/order/<int:id>',views.order_detail,name= 'order-detail'),
  
  # make default address
  
  path('delete-address/<int:id>/', views.delete_address, name="delete-address"),
  
  path('make-default-address/', views.make_address_default,name= 'make-default-address'),
  
  # place order
  
  path('checkout/place-order/', views.place_order,name= 'place-order'),
  
  
  # wallet_order_place
  
  path('wallet-order-place',views.wallet_order_place, name="wallet-order-place"),
  
  
  # paypal path
  
  path('paypal/', include('paypal.standard.ipn.urls')),
  
  # payment completed
  
   path('payment-completed/', views.payment_completed_view,name= 'payment-completed'),
   
   path('payment-failed/', views.payment_failed_view,name= 'payment-failed'),
   
   
  #  add coupon
  
  # path('add-coupon/',views.add_coupon,name='add-coupon')
  # add to wishlist
  
  path('wishlist/',views.wishlist_view, name="wishlist"),
  
  
  path('add-to-wishlist/', views.add_to_wishlist, name="add-to-wishlist"),
  
  
  # remove from wishlist
  
  path("remove-from-wishlist", views.remove_wishlist, name="remove-from-wishlist"),
  
  
  path("referral-coupon/",views.referral_coupon, name="referral-coupon"),
  
  path("about-us/",views.about_us, name="about-us"),
   
  path("contact/",views.contact, name="contact"),
  
  path("helloworld/", views.hello_world, name='hello_world'),
  
  path("reviewedit/<int:id>", views.edit_review, name='reviewedit')
  
]