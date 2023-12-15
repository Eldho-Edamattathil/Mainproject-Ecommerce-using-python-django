from app1.models import Product,ProductImages,Category,wishlist_model
from django.shortcuts import render,redirect
from django.db.models import Min, Max
from django.contrib import messages



def default(request):
  categories = Category.objects.filter(is_blocked =False)
  min_max_price = Product.objects.aggregate(Min("price"),Max('price'))
  
  
  try:
    wishlist=wishlist_model.objects.filter(user=request.user)
  except:
    # messages.warning(request,"You need to login to access wishlist")
    wishlist=0
  
  return {
    "categories":categories,
    "min_max_price":min_max_price,
    "wishlist":wishlist
    
  }
  
  
# def default(request):
#     categories = Category.objects.filter(is_blocked =False)
#     cart_total_amount = 0

#     if 'cart_data_obj' in request.session:
#         cart_data = request.session.get('cart_data_obj', {})

#         for p_id, item in cart_data.items():
#             try:
#                 # Split the price string into individual prices and convert to float
#                 prices = [float(price) for price in item.get('price', '').split()]
#                 print(prices)
#                 # Sum up the individual prices
#                 total_price = sum(prices)
#                 print(total_price)
#                 qty = int(item.get('qty', 0))
#                 cart_total_amount += qty * total_price
#             except (ValueError, TypeError):
#                 # Handle conversion errors if qty or total_price is not a valid number
#                 pass

#         return  {
#             'cart_data': cart_data,
#             'totalcartitems': len(cart_data),
#             'cart_total_amount': cart_total_amount,
#             "categories":categories
#         }
    
    