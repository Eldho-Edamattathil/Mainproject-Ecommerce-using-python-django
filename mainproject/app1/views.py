from django.db.models import Count,Avg
from django.shortcuts import render,redirect
from app1.models import Product,ProductImages,Category,Variants,Size,Cart,CartItem,CartOrder,CartOrderItems,Address,UserDetails,Coupon,wishlist_model,wallet,ProductReview,ProductOffer,CategoryOffer
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.utils import timezone
from admindash.forms import CouponForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core import serializers
from userauths.models import User
from app1.forms import ProductReviewForm
from django.http import Http404





@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    # code = str(kwargs.get('ref_code'))
    # if code:
    #     code = str(code)
    #     try:
    #         profile = UserDetails.objects.get(code=code)
    #         request.session['ref_profile'] = profile.id
    #         print("id", profile.id)
    #     except UserDetails.DoesNotExist:
    #         pass
    #     print(request.session.get_expiry_date())
    
    blocked_categories =Category.objects.filter(is_blocked =True)
    products = Product.objects.filter(featured = True, status =True).exclude(category__in=blocked_categories)
    latest = Product.objects.filter(status=True).order_by("-id")[:10]
    categories =Category.objects.filter(is_blocked =False)
    try:
        
        discount_offer = ProductOffer.objects.get(active=True)
    except ProductOffer.DoesNotExist:
        discount_offer = None
    if discount_offer:
        current_date = timezone.now()
        if current_date > discount_offer.end_date or current_date < discount_offer.start_date:
            discount_offer.active = False
            discount_offer.save()
    
                        
    try:
        
        discounted_offer = CategoryOffer.objects.filter(active=True)
    except ProductOffer.DoesNotExist:
        discounted_offer = None
    if discounted_offer:
        for dis in discounted_offer:
            products_with_discount = Product.objects.filter(category=dis.category, status=True)
            current_date = timezone.now()
            if current_date > dis.end_date or current_date < dis.start_date:
                dis.active = False
                dis.save()
    context = {
        "products":products,
        "latest":latest,
        "categories":categories,
        "discount_offer":discount_offer,
        "discounted_offer":discounted_offer
    }
    return render(request, 'app1/index.html',context)


def product_list(request):
    blocked_categories =Category.objects.filter(is_blocked =True)
    products = Product.objects.filter(status =True).exclude(category__in=blocked_categories)
    categories =Category.objects.filter(is_blocked =False)
    p=Paginator(Product.objects.filter(status =True).exclude(category__in=blocked_categories),10)
    page=request.GET.get('page')
    productss=p.get_page(page)
    try:
        discount_offer = ProductOffer.objects.get(active=True)
    except ProductOffer.DoesNotExist:
        discount_offer = None
        
    try:
        
        discounted_offer = CategoryOffer.objects.filter(active=True)
    except ProductOffer.DoesNotExist:
        discounted_offer = None
    if discounted_offer:
        for dis in discounted_offer:
            products_with_discount = Product.objects.filter(category=dis.category, status=True)
            current_date = timezone.now()
            if current_date > dis.end_date:
                dis.active = False
                dis.save()
    
    
    context = {
        "products":products,
        "categories":categories,
        "productss":productss,
        'discount_offer':discount_offer,
        "discounted_offer":discounted_offer
    }
    
    return render(request,'app1/product_list.html', context)


def category_list(request):
    category = Category.objects.filter(is_blocked=False)
    
    
    context ={
        "category":category,
       
    }
    return render(request,'app1/category_list.html', context )



def category_product_list(request, cid):
    category = Category.objects.get(cid=cid)
    product = Product.objects.filter(category=category,status =True)
    
    try:
        
        discount_offer = ProductOffer.objects.get(active=True)
    except ProductOffer.DoesNotExist:
        discount_offer = None
    
    
                        
    try:
        
        discounted_offer = CategoryOffer.objects.filter(active=True)
    except ProductOffer.DoesNotExist:
        discounted_offer = None
    if discounted_offer:
        for dis in discounted_offer:
            products_with_discount = Product.objects.filter(category=dis.category, status=True)
            current_date = timezone.now()
            if current_date > dis.end_date:
                dis.active = False
                dis.save()
    
    
    
    context ={
        "category":category,
        "product":product,
        "discount_offer":discount_offer,
        "discounted_offer":discounted_offer
    }
    
    return render(request,'app1/category_product_list.html', context)


# def product_detail(request,pid):
#     product = Product.objects.get(pid = pid)
#     p_image =product.p_images.all()
#     category = Category.objects.all()
#     products = Product.objects.filter(category=product.category).exclude(pid=pid)[:4]
#     sizes = Size.objects.all()
    
#     context={
#         "product":product,
#         "p_image":p_image,
#         "category":category,
#         "products":products,
#         "sizes": sizes 
        
        
        
#     }
    
    
    
#     return render (request,'app1/product_detail.html',context)

def product_detail(request, pid):
    product = get_object_or_404(Product, pid=pid)
    p_image = product.p_images.all()
    category = Category.objects.all()
    products = Product.objects.filter(category=product.category).exclude(pid=pid)[:4]
    sizes = Size.objects.all()
    variants = Variants.objects.filter(product=product)
    review=ProductReview.objects.filter(product=product).order_by("-date")
    average_rating =ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))
    try:
        
        discount_offer = ProductOffer.objects.get(active=True)
    except ProductOffer.DoesNotExist:
        discount_offer = None
    
    
                        
    try:
        
        discounted_offer = CategoryOffer.objects.filter(active=True)
    except ProductOffer.DoesNotExist:
        discounted_offer = None
    if discounted_offer:
        for dis in discounted_offer:
            products_with_discount = Product.objects.filter(category=dis.category, status=True)
            current_date = timezone.now()
            if current_date > dis.end_date:
                dis.active = False
                dis.save()
    
    
    review_form=ProductReviewForm()
    

    context = {
        "product": product,
        "p_image": p_image,
        'review_form':review_form,
        "category": category,
        "products": products,
        "sizes": sizes,
        'review':review,
        'average_rating':average_rating,
        "variants": variants,
        "discount_offer":discount_offer,
        "discounted_offer":discounted_offer
        
    }

    return render(request, 'app1/product_detail.html', context)

# Review View

# def add_ajax_review(request,pid):
#     product=Product.objects.get(pk=pid)
#     user=request.user
    
#     review = ProductReview.objects.create(
#         user=user,
#         product=product,
#         review=request.POST['review'],
#         rating=request.POST['rating'],
#     )
    
#     context={
#         "user":user.username,
#         "review":request.POST['review'],
#         "rating":request.POST['rating']
        
        
        
#     }
    
#     average_reviews=ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))
    
    
#     return JsonResponse(
#         {
        
#         'bool':True,
#         'context':context,
#         'average_reviews':average_reviews
#         }
    
#         )

# def add_ajax_review(request, pid):
#     if request.method == 'POST':
#         try:
#             product = Product.objects.get(pk=pid)
#             user = request.user
#             review_text = request.POST.get('review', '')
#             rating = float(request.POST.get('rating', 0))

#             # Create a new ProductReview
#             review = ProductReview.objects.create(
#                 user=user,
#                 product=product,
#                 review=review_text,
#                 rating=rating,
#             )

#             # Calculate average rating for the product
#             average_reviews = ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg("rating"))

#             context = {
#                 "user": user.username,
#                 "review": review_text,
#                 "rating": rating,
#             }
            
            

#             return JsonResponse({
#                 'success': True,
#                 'context': context,
#                 'average_reviews': average_reviews['avg_rating'] if average_reviews['avg_rating'] else 0,
#             })

#         except Product.DoesNotExist:
#             return JsonResponse({'success': False, 'error': 'Product does not exist'})

#     return JsonResponse({'success': False, 'error': 'Invalid request method'})

def add_ajax_review(request, pid):
    if not request.user.is_authenticated:
        messages.warning(request,"Please log in to write review")
        # return redirect("app1:index")
        return JsonResponse({'redirect': '/app1/index/'})
        
    product = get_object_or_404(Product, pk=pid)
    image=UserDetails.objects.filter(user=request.user)
    print(image)
    user = request.user
    
    
    has_purchased = CartOrderItems.objects.filter(
        order__user=user,
        item=product.title,  
    ).exists()
    

    if not has_purchased:
        messages.warning(request, "You can only write a review for products you have purchased.")
        return JsonResponse({'bool': False})

    try:
        
        review = ProductReview.objects.create(
            user=user,
            product=product,
            review=request.POST['review'],
            rating=request.POST['rating'],
        )

        context = {
            "user": user.username,
            # "image":image.image,
            "review": request.POST['review'],
            "rating": request.POST['rating'],
        }

        average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))

        # Convert the Decimal to a float for JSON serialization
        average_rating = float(average_reviews['rating']) if average_reviews['rating'] else 0.0

        return JsonResponse({
            'bool': True,
            'context': context,
            'average_reviews': average_rating,
        })

    except Exception as e:
        return JsonResponse({'bool': False, 'error': str(e)})


    

def search_view(request):
    query =request.GET.get('q')
    print(query)
    
    products =Product.objects.filter(title__icontains =query)
    print(products)
    
    context ={
        'products':products,
        'query': query
        
    }
    
    return render(request,'app1/search.html',context)



    
def filter_product(request):    
    try:
            categories = request.GET.getlist('category[]')
            print("Selected Categories:", categories)

            min_price= request.GET['min_price']
            max_price= request.GET['max_price']
            
            products = Product.objects.filter(status=True).order_by('-id').distinct()
            
            products=products.filter(price__gte=min_price)
            products=products.filter(price__lte=max_price)
            print("All Products:", products)
            print("Selected Categories:", categories)

            if len(categories) > 0:
                products = products.filter(category__cid__in=categories).distinct()
                print("Filtered Product:", products)

            data = render_to_string('app1/async/product-list.html', {"products": products})
            return JsonResponse({"data": data})
    except Exception as e:
            return JsonResponse({"error": str(e)})


    

    
    
        
    



# working cart

def add_to_cart(request):
    product_id = str(request.GET['id'])
    
    cart_product = {
        product_id: {
            'title': request.GET['title'],
            'qty': request.GET['qty'],
            'price': request.GET['price'],
            'pid': request.GET['pid'],
            'image': request.GET['image'],
        }
    }
    
    
    
        
    
    
    

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']

        if product_id in cart_data:
            # Product already exists in the cart
            return JsonResponse({
                "message": "Product already in the cart",
                'totalcartitems': len(cart_data),
                'already_in_cart': True
            })
        else:
            # Product is not in the cart, add it
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product

    return JsonResponse({
        "message": "Product added to the cart",
        'totalcartitems': len(request.session['cart_data_obj']),
        'already_in_cart': False
    })














# existing cart view

# modified

def cart_view(request):
    cart_total_amount = 0
    final_money=0
    money=0
    print(request.session.items())
    current_date = timezone.now().date()
    available_coupons = Coupon.objects.filter(active=True, active_date__lte=current_date, expiry_date__gte=current_date)
    
    
       
            
        
        
    
    
    
    if 'cart_data_obj' in request.session:
        cart_data = request.session.get('cart_data_obj',{})
        print(cart_data)

        for p_id, item in cart_data.items():
            try:
                # Split the price string into individual prices and convert to float
                prices = [float(price) for price in item.get('price', '').split()]
                print(prices)
                
                # Sum up the individual prices
                total_price = sum(prices)
                print(total_price)
                qty = int(item.get('qty', 0))
                cart_total_amount += qty * total_price
            except (ValueError, TypeError):
                # Handle conversion errors if qty or total_price is not a valid number
                pass
            
           
            
            
        # Coupon
        if request.method == 'POST':
            coupon_form = CouponForm(request.POST)  # Instantiate the coupon form with the POST data

            if coupon_form.is_valid():
                coupon_code = coupon_form.cleaned_data['code']
                print(coupon_code)
                
                try:
                    # Assuming you have a Coupon model
                    coupon = Coupon.objects.get(code__iexact=coupon_code, active=True)
                    
                    # Check if the coupon is within its active and expiry dates
                    current_date = timezone.now().date()
                    if current_date < coupon.active_date or current_date > coupon.expiry_date:
                        messages.warning(request, 'Invalid coupon code or expired')
                    else:
                        # Apply the coupon discount to the cart total
                        money=cart_total_amount
                        cart_total_amount -= (cart_total_amount * coupon.discount) / 100
                        request.session['applied_coupon'] = cart_total_amount
                        final_money=money-cart_total_amount
                        messages.success(request, f'Coupon "{coupon.code}" applied successfully')

                except Coupon.DoesNotExist:
                    messages.warning(request, 'Invalid coupon code')
        else:
            coupon_form = CouponForm()
            
            
        
        
        

        return render(request, 'app1/cart.html', {
            'cart_data': cart_data,
            'final_money':final_money,
            'money':money,
            'totalcartitems': len(cart_data),
            'cart_total_amount': cart_total_amount,
            'coupon_form': coupon_form, 
            'available_coupons':available_coupons 
        })
    
    print("hello123")
    messages.warning(request, "Your cart is empty")
    return redirect('app1:index')
     
    
       
    
    
    

    
# def cart_view(request):
#     cart_total_amount = 0

#     if 'cart_data_obj' in request.session:
#         cart_data = request.session.get('cart_data_obj', {})
#         print(cart_data)

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
            
#         # Coupon
#         if request.method == 'POST':
#             coupon_form = CouponForm(request.POST)  # Instantiate the coupon form with the POST data

#             if coupon_form.is_valid():
#                 coupon_code = coupon_form.cleaned_data['code']
#                 print(coupon_code)
#                 try:
#                     # Assuming you have a Coupon model
#                     coupon = Coupon.objects.get(code__iexact=coupon_code, active=True)
                    
#                     # Check if the coupon is within its active and expiry dates
#                     current_date = timezone.now().date()
#                     if current_date < coupon.active_date or current_date > coupon.expiry_date:
#                         messages.warning(request, 'Invalid coupon code or expired')
#                     else:
#                         # Apply the coupon discount to the cart total
#                         cart_total_amount -= (cart_total_amount * coupon.discount) / 100
#                         request.session['applied_coupon'] = cart_total_amount
#                         messages.success(request, f'Coupon "{coupon.code}" applied successfully')

#                 except Coupon.DoesNotExist:
#                     messages.warning(request, 'Invalid coupon code')
        
#         else:
#             coupon_form = CouponForm()
            
#     else:
#         messages.warning(request, "Your cart is empty")
#         return redirect('app1:index')

#     return render(request, 'app1/cart.html', {
#         'cart_data': cart_data,
#         'totalcartitems': len(cart_data),
#         'cart_total_amount': cart_total_amount,
#         'coupon_form': coupon_form,  # Pass the coupon form to the template
#     })

#     # messages.warning(request, "Your cart is empty")
#     # return redirect('app1:index')




# def cart_view(request):
#     cart_total_amount = 0

#     if 'cart_data_obj' in request.session:
#         cart_data = request.session.get('cart_data_obj', {})
#         print(cart_data)

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
            
            
             
            
#         # coupon
#             if request.method == 'POST':
#                 coupon_form = CouponForm(request.POST)  # Instantiate the coupon form with the POST data

#                 if coupon_form.is_valid():
#                     coupon_code = coupon_form.cleaned_data['code']
#                     print(coupon_code)
#                     try:
#                         # Assuming you have a Coupon model
#                         coupon = Coupon.objects.get(code__iexact=coupon_code, active=True)
                        
#                         # Check if the coupon is within its active and expiry dates
#                         current_date = timezone.now().date()
#                         if current_date < coupon.active_date or current_date > coupon.expiry_date:
#                             messages.warning(request, 'Invalid coupon code or expired')
#                         else:
#                             # Apply the coupon discount to the cart total
#                             cart_total_amount -= (cart_total_amount * coupon.discount) / 100
#                             request.session['applied_coupon']=cart_total_amount
#                             messages.success(request, f'Coupon "{coupon.code}" applied successfully')
                            

#                     except Coupon.DoesNotExist:
#                         messages.warning(request, 'Invalid coupon code')
                

#             else:
#                 coupon_form = CouponForm()
                
            

#         return render(request, 'app1/cart.html', {
#             'cart_data': cart_data,
#             'totalcartitems': len(cart_data),
#             'cart_total_amount': cart_total_amount,
#             # 'coupon_form': coupon_form,  # Pass the coupon form to the template
#         })
    
#     messages.warning(request, "Your cart is empty")
#     return redirect('app1:index')
#     #     return render(request, 'app1/cart.html', {
#     #         'cart_data': cart_data,
#     #         'totalcartitems': len(cart_data),
#     #         'cart_total_amount': cart_total_amount
#     #     })
#     # else:
   
    
# # def cart_view(request):
#     user = request.user
#     cart_total_amount = 0

#     try:
#         cart = user.cart
#     except Cart.DoesNotExist:
#         cart = None

#     if cart:
#         cart_items = CartItem.objects.filter(cart=cart)

#         for cart_item in cart_items:
#             print(f"Product Price: {cart_item.product.price}, Quantity: {cart_item.quantity}")
#             total_price = float(cart_item.product.price) * cart_item.quantity
#             cart_total_amount += total_price
            

#         return render(request, 'app1/cart.html', {
#             'cart_items': cart_items,
#             'totalcartitems': cart_items.count(),
#             'cart_total_amount': cart_total_amount
#         })
#     else:
#         messages.warning(request, "Your cart is empty")
#         return redirect('app1:index')   
    


# db cart view
# def cart_view(request):
#     cart_total_amount = 0

#     if request.user.is_authenticated:
#         # Retrieve products from the database for authenticated users
#         user_cart, created = Cart.objects.get_or_create(user=request.user)
#         cart_items = CartItem.objects.filter(cart=user_cart)

#         # Save the products to the session
#         cart_data = {}
#         for cart_item in cart_items:
#             product_id = str(cart_item.product.id)
#             cart_data[product_id] = {
#                 'title': cart_item.product.title,
#                 'qty': cart_item.quantity,
#                 'price': str(cart_item.product.price),
#                 'pid': str(cart_item.product.pid),
#                 'image': str(cart_item.product.image),
#             }

#             try:
#                 # Calculate total price for the cart view
#                 total_price = float(cart_item.product.price) * cart_item.quantity
#                 cart_total_amount += total_price
#             except (ValueError, TypeError):
#                 # Handle conversion errors if quantity or total_price is not a valid number
#                 pass

#         # Save the updated cart data to the session
#         request.session['cart_data_obj'] = cart_data

#         return render(request, 'app1/cart.html', {
#             'cart_data': cart_data,
#             'totalcartitems': len(cart_data),
#             'cart_total_amount': cart_total_amount
#         })
#     else:
#         # Handle the case for anonymous users
#         messages.warning(request, "Your cart is empty")
#         return redirect('app1:index')


def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        
        if product_id in cart_data:
            del cart_data[product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']

        for p_id, item in cart_data.items():
            try:
                # Split the price string into individual prices and convert to float
                prices = [float(price) for price in item.get('price', '').split()]
                # Sum up the individual prices
                total_price = sum(prices)
                qty = int(item.get('qty', 0))
                cart_total_amount += qty * total_price
            except (ValueError, TypeError):
                # Handle conversion errors if qty or total_price is not a valid number
                pass
            
    context = render_to_string("app1/async/cart-list.html", {
        'cart_data': cart_data,
        'totalcartitems': len(cart_data),
        'cart_total_amount': cart_total_amount
    })

    return JsonResponse({"data": context, 'totalcartitems': len(cart_data)})



def update_from_cart(request):
    product_id = str(request.GET.get('id'))
    product_qty = int(request.GET.get('qty', 0))

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']

        if product_id in cart_data:
            cart_data[product_id]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']

        for p_id, item in cart_data.items():
            try:
                # Split the price string into individual prices and convert to float
                prices = [float(price) for price in item.get('price', '').split()]
                # Sum up the individual prices
                total_price = sum(prices)
                qty = int(item.get('qty', 0))
                cart_total_amount += qty * total_price
            except (ValueError, TypeError):
                # Handle conversion errors if qty or total_price is not a valid number
                pass

    context = render_to_string("app1/async/cart-list.html", {
        'cart_data': cart_data,
        'totalcartitems': len(cart_data),
        'cart_total_amount': cart_total_amount
    })

    return JsonResponse({"data": context, 'totalcartitems': len(cart_data)})





    
   
   


def checkout_view(request):
    
    
    
    cart_total_amount = 0
    total_amount = 0

    if not request.user.is_authenticated:
        # Handle anonymous user (redirect to login, show a message, etc.)
        messages.warning(request, "Please log in to complete the checkout.")
        return redirect('userauths:login')  # Adjust the redirect URL as needed

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        print(cart_data)

        # Calculate total_amount for the entire order
        for p_id, item in cart_data.items():
            try:
                # Split the price string into individual prices and convert to float
                prices = [float(price) for price in item.get('price', '').split()]
                # Sum up the individual prices
                total_price = sum(prices)
                qty = int(item.get('qty', 0))
                total_amount += qty * total_price
            except (ValueError, TypeError):
                # Handle conversion errors if qty or total_price is not a valid number
                pass

# coupon applied total amount

        applied_coupon = request.session.get('applied_coupon', None)
    # discount=total_amount-applied_coupon
    # print(discount)

        if applied_coupon is not None:
                # If a coupon is applied, use the stored cart_total_amount
            cart_total_amount = applied_coupon
            del request.session['applied_coupon']
            request.session['invoice_amt'] = cart_total_amount
            discount=total_amount-cart_total_amount
            request.session['discount']=discount

            
        else:
                # If no coupon is applied, calculate the cart_total_amount from the cart_data
            cart_total_amount = 0    
            # if 'cart_data_obj' in request.session:
            #     cart_data = request.session['cart_data_obj']

            for p_id, item in cart_data.items():
                try:
                    prices = [float(price) for price in item.get('price', '').split()]
                    total_price = sum(prices)
                    qty = int(item.get('qty', 0))
                    cart_total_amount += qty * total_price
                except (ValueError, TypeError):
                    pass


            print(cart_total_amount)
            request.session['cart_total_amount'] = cart_total_amount
            discount=total_amount-cart_total_amount





        
        try:
            active_address = Address.objects.get(user=request.user, status=True)
        except Address.DoesNotExist:
            messages.warning(request, "Please select an address before proceeding.")
            return redirect('app1:dashboard')  # Redirect to the address selection page

       

        
        
    host=request.get_host()
    paypal_dict={
        'business':settings.PAYPAL_RECEIVER_EMAIL,
        'amount':cart_total_amount,
        'item_name':'Order-Item-No-'+ str(CartOrder.id),
        'invoice':'INVOICE_NO-'+ str(CartOrder.id),
        'currency_code':"USD",
        'notify_url':'http://{}{}'.format(host, reverse("app1:paypal-ipn")),
        'return_url':'http://{}{}'.format(host, reverse("app1:payment-completed")),
        'cancel_url':'http://{}{}'.format(host, reverse("app1:payment-failed")),
        
        
    }
    
    paypal_payment_button=PayPalPaymentsForm(initial=paypal_dict)
    
    if paypal_payment_button in request.POST:
        print("payment done")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    print(cart_total_amount)
    return render(request, 'app1/checkout.html', {
            'cart_data': cart_data,
            'totalcartitems': len(cart_data),
            'cart_total_amount': cart_total_amount,
            'active_address':active_address,
            'paypal_payment_button':paypal_payment_button,
            'discount':discount,
            'total_amount':total_amount
        })
    return HttpResponse("No items in the cart. Please add items before checking out.")








    

    
    
    
    

    
    
    












# Customer Dashboard

def customer_dashboard(request):
    if not request.user.is_authenticated:
        # Handle anonymous user (redirect to login, show a message, etc.)
        messages.warning(request, "Please log in to access Dashboard.")
        return redirect('app1:index')
    
        
    orders=CartOrder.objects.filter(user=request.user).order_by("-id")
    
    
    wallet_debits = []
    wallet_credits = []
    for order in orders:
       
        if order.product_status == 'cancelled':
            
            if order.wallet_status:
                
                wallet_credits.append(order)
                
        else:
            
            if order.wallet_status:
               
                wallet_debits.append(order)
                
    wallet_debits_qs = CartOrder.objects.filter(user=request.user, wallet_status=True, product_status='processing').order_by('-id')

    
    wallet_credits_qs = CartOrder.objects.filter(user=request.user, wallet_status=True, product_status='cancelled').order_by('-id')
    
    
    
    
    
    user_account=User.objects.filter(email=request.user)
    
    
    address = Address.objects.filter(user=request.user)
    user_profile, created = UserDetails.objects.get_or_create(user=request.user)

    if created:
        messages.success(request, 'UserDetails created successfully.')
    
    if request.method == 'POST':
        address =request.POST['address']
        mobile = request.POST['phone']
        
        new_address =Address.objects.create (
            user =request.user,
            address =address,
            mobile =mobile
        )
        messages.success(request,'Address Added Successfully')
        return redirect("app1:dashboard")
    else:
        print("Error")
        
    wallet_amt=wallet.objects.filter(user=request.user)
    
    context ={
        'user_profile':user_profile,
        'orders':orders,
        'address':address,
        'wallet_amt':wallet_amt,
        # 'wallet_orders':wallet_orders,
        'wallet_debits_qs':wallet_debits_qs,
        'wallet_credits_qs':wallet_credits_qs,
        'user_account':user_account,
        # 'latest_order':latest_order
    }
    
    return render(request,'app1/dashboard.html',context)

    


def order_detail(request, id):
    # Use get_object_or_404 to ensure that the order exists or return a 404 response
    order = get_object_or_404(CartOrder, user=request.user, id=id)
    print(order)

    # Use filter based on the specific order instance
    products = CartOrderItems.objects.filter(order=order)

    context = {
        'products': products,
    }

    return render(request, 'app1/order-detail.html', context)



def make_address_default(request):
    id =request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id =id).update(status=True)
    return JsonResponse({'boolean':True})





def place_order(request):
    cart_total_amount = 0
    total_amount = 0
    
    
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        for p_id, item in cart_data.items():
            print(item)
            products=Product.objects.filter(title=item['title'])
            for p in products:
                p.stock_count=int(p.stock_count) - int(item['qty'])
                p.save() 
                
                
                
                
    # store data in database
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        print(cart_data)

        # Calculate total_amount for the entire order
        for p_id, item in cart_data.items():
            try:
                # Split the price string into individual prices and convert to float
                prices = [float(price) for price in item.get('price', '').split()]
                # Sum up the individual prices
                total_price = sum(prices)
                qty = int(item.get('qty', 0))
                total_amount += qty * total_price
            except (ValueError, TypeError):
                # Handle conversion errors if qty or total_price is not a valid number
                pass

        if request.user.is_authenticated:
            # Create CartOrder for the entire order only if the user is authenticated
            order = CartOrder.objects.create(
                user=request.user,
                price=total_amount
            )

            # Create CartOrderItems for each product in the cart
            for p_id, item in cart_data.items():
                try:
                    prices = [float(price) for price in item.get('price', '').split()]
                    total_price = sum(prices)
                    qty = int(item.get('qty', 0))
                    cart_total_amount += qty * total_price

                    # Create CartOrderItems for each product
                    CartOrderItems.objects.create(
                        order=order,
                        invoice_no="INVOICE_NO-" + str(order.id),
                        item=item['title'],
                        image=item['image'],
                        qty=qty,
                        price=item['price'],
                        total=qty * total_price
                    )
                except (ValueError, TypeError):
                    pass
    
    
    #till here
    del request.session['cart_data_obj']
        
    
             
    

    return render(request, 'app1/place-order.html')




# wallet order place


def wallet_order_place(request):
    cart_total_amount = 0
    total_amount = 0
    
    
    
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        for p_id, item in cart_data.items():
            print(item)
            products=Product.objects.filter(title=item['title'])
            for p in products:
                p.stock_count=int(p.stock_count) - int(item['qty'])
                p.save() 
                
    # user_wallet = get_object_or_404(wallet, user=request.user)
    user_wallet, created = wallet.objects.get_or_create(user=request.user)

    print(user_wallet.Amount)
        
                
                
    # store data in database
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        print(cart_data)

       
        applied_coupon = request.session.get('invoice_amt', None)
        
    

        if applied_coupon is not None:
            del request.session['invoice_amt']
            total_amount = applied_coupon
            
           
            
        
        
        else:
            total_amount=0
            for p_id, item in cart_data.items():
                try:
                    
                    prices = [float(price) for price in item.get('price', '').split()]
                    
                    total_price = sum(prices)
                    qty = int(item.get('qty', 0))
                    total_amount += qty * total_price
                except (ValueError, TypeError):
                  
                    pass
        total_amount_decimal = Decimal(str(total_amount))

        if user_wallet.Amount < total_amount:
            messages.error(request, "Wallet money is not enough to purchase this product")
            return redirect("app1:checkout")
        else:
            
            user_wallet.Amount-=total_amount_decimal
            user_wallet.save()
            messages.success(request,f"{total_amount_decimal} has been deducted from your wallet" )
                
            

        if request.user.is_authenticated:
           
            order = CartOrder.objects.create(
                user=request.user,
                price=total_amount,
                paid_status=True,
                wallet_status=True,
            )
           
            for p_id, item in cart_data.items():
                try:
                    prices = [float(price) for price in item.get('price', '').split()]
                    total_price = sum(prices)
                    qty = int(item.get('qty', 0))
                    cart_total_amount += qty * total_price

                    
                    CartOrderItems.objects.create(
                        order=order,
                        invoice_no="INVOICE_NO-" + str(order.id),
                        item=item['title'],
                        image=item['image'],
                        qty=qty,
                        price=item['price'],
                        total=qty * total_price
                    )
                except (ValueError, TypeError):
                    pass
    
                
    
        del request.session['cart_data_obj']
    else:
        return redirect("app1:index")
    
        
   
            
    print(user_wallet.Amount)
           
    return render(request, 'app1/place-order.html',{'user_wallet.Amount':user_wallet.Amount})








# PAYPAL

def payment_completed_view(request):
    
   
    cart_total_amount = 0
    total_amount = 0
    
    
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        for p_id, item in cart_data.items():
            print(item)
            products=Product.objects.filter(title=item['title'])
            for p in products:
                p.stock_count=int(p.stock_count) - int(item['qty'])
                p.save() 
                
   
        
                
                
    # store data in database
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        print(cart_data)
        
        applied_coupon = request.session.get('invoice_amt', None)
        discount=request.session.get('discount', None)

        if applied_coupon is not None:
            # If a coupon is applied, use the stored cart_total_amount
            total_amount = applied_coupon
            del request.session['invoice_amt']
            del request.session['discount']
        else:

            total_amount=0
            discount=0
            for p_id, item in cart_data.items():
                try:
                    # Split the price string into individual prices and convert to float
                    prices = [float(price) for price in item.get('price', '').split()]
                    # Sum up the individual prices
                    total_price = sum(prices)
                    qty = int(item.get('qty', 0))
                    total_amount += qty * total_price
                except (ValueError, TypeError):
                    # Handle conversion errors if qty or total_price is not a valid number
                    pass
        
        
            
        

        if request.user.is_authenticated:
            # Create CartOrder for the entire order only if the user is authenticated
            order = CartOrder.objects.create(
                user=request.user,
                price=total_amount,
                paid_status=True
            )

            # Create CartOrderItems for each product in the cart
            
            # coupon check
            # applied_coupon = request.session.get('invoice_amt', None)
            # discount=request.session.get('discount', None)

            # if applied_coupon is not None:
            #     # If a coupon is applied, use the stored cart_total_amount
            #     cart_total_amount = applied_coupon
            #     del request.session['invoice_amt']
            #     del request.session['discount']
            
            
            # till here
            
            
            
            
            
            for p_id, item in cart_data.items():
                try:
                    prices = [float(price) for price in item.get('price', '').split()]
                    total_price = sum(prices)
                    qty = int(item.get('qty', 0))
                    cart_total_amount += qty * total_price

                    # Create CartOrderItems for each product
                    CartOrderItems.objects.create(
                        order=order,
                        invoice_no="INVOICE_NO-" + str(order.id),
                        item=item['title'],
                        image=item['image'],
                        qty=qty,
                        price=item['price'],
                        total=qty * total_price
                    )
                except (ValueError, TypeError):
                    pass
        
            
        #till here
        del request.session['cart_data_obj']
    else:
        return redirect('app1:index')
            
        
        
        
        
        
    
    # TILL HERE
    return render(request, 'app1/payment-completed.html',{
            'cart_data': cart_data,
            'totalcartitems': len(cart_data),
            'cart_total_amount': cart_total_amount,
            'total_amount':total_amount,
            'discount':discount
            
        
        })


def payment_failed_view(request):
    return render(request, 'app1/payment-failed.html')




# wishlist

@login_required
def wishlist_view(request):
    
    wishlist=wishlist_model.objects.filter(user=request.user)
    
    
    if not wishlist:
        # If the wishlist is empty, redirect to the index view with a message
        messages.warning(request," wishlist is empty")
        return redirect("app1:index") 
    
    
    context={
        'w':wishlist
    }
    
    
    return render(request,'app1/wishlist.html',context)

@login_required
def add_to_wishlist(request):
    product_id=request.GET['id']
    product=Product.objects.get(id=product_id)
    
    context={
        
    }
    
    wishlist_count=wishlist_model.objects.filter(product=product,user=request.user).count()
    print(wishlist_count)
    
    if wishlist_count > 0:
        context={
            "bool":True
        }
        
    else:
        new_wishlist=wishlist_model.objects.create(
            product=product,
            user=request.user
        )
        context={
            "bool":True
        }
    return JsonResponse(context)



# remove from wishlist

def remove_wishlist(request):
    pid =request.GET['id']
    wishlist= wishlist_model.objects.filter(user=request.user)
    
    wishlist_d=wishlist_model.objects.get(id=pid)
    
    delete_product=wishlist_d.delete()
    
    context={
        "bool":True,
        "w":wishlist
        
    }
    if not wishlist_d:
        messages.warning(request,"Nothiing")
    
    
    wishlist_json=serializers.serialize('json', wishlist)
    data= render_to_string("app1/async/wishlist-list.html", context)
    
    
    return JsonResponse({"data":data,"w":wishlist_json})







