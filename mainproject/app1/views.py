from django.db.models import Count
from django.shortcuts import render,redirect
from app1.models import Product,ProductImages,Category,Variants,Size
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.contrib import messages



@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    # if request.user.is_authenticated:
    #     # Clear the OTP session if it exists
    #     if 'otp' in request.session:
    #         del request.session['otp']
    blocked_categories =Category.objects.filter(is_blocked =True)
    products = Product.objects.filter(featured = True, status =True).exclude(category__in=blocked_categories)
    latest = Product.objects.filter(status=True).order_by("-id")[:10]
    categories =Category.objects.filter(is_blocked =False)
   

    
    context = {
        "products":products,
        "latest":latest,
        "categories":categories
    }
    return render(request, 'app1/index.html',context)


def product_list(request):
    blocked_categories =Category.objects.filter(is_blocked =True)
    products = Product.objects.filter(status =True).exclude(category__in=blocked_categories)
    categories =Category.objects.filter(is_blocked =False)
    p=Paginator(Product.objects.filter(status =True).exclude(category__in=blocked_categories),10)
    page=request.GET.get('page')
    productss=p.get_page(page)
    
    context = {
        "products":products,
        "categories":categories,
        "productss":productss
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
    
    
    context ={
        "category":category,
        "product":product
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
    

    context = {
        "product": product,
        "p_image": p_image,
        "category": category,
        "products": products,
        "sizes": sizes,
        "variants": variants  # Pass variants to the template
    }

    return render(request, 'app1/product_detail.html', context)


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


# def filter_product(request):
    categories =request.GET.getlist('Category[]')
    
    products =Product.objects.filter(status=True).order_by('-id').distinct()
    
    if len(categories) > 0:
        products=products.filter(category__id__in=categories).distinct()
        
    data =render_to_string('app1/async/product-list.html',{"products":products})
    return JsonResponse ({"data":data})
    
def filter_product(request):    
    try:
            categories = request.GET.getlist('category[]')
            print("Selected Categories:", categories)

            products = Product.objects.filter(status=True).order_by('-id').distinct()
            print("All Products:", products)
            print("Selected Categories:", categories)

            if len(categories) > 0:
                products = products.filter(category__cid__in=categories).distinct()
                print("Filtered Product:", products)

            data = render_to_string('app1/async/product-list.html', {"products": products})
            return JsonResponse({"data": data})
    except Exception as e:
            return JsonResponse({"error": str(e)})

# def filter_product(request):
#     try:
#         # Get selected categories
#         categories = request.GET.getlist('category[]')
#         print("Selected Categories:", categories)

#         # Get price range
#         min_price = Decimal(request.GET.get('min_price', 0))
#         max_price = Decimal(request.GET.get('max_price', float('inf')))
#         print("Price Range:", min_price, max_price)

#         # Filter products based on status and categories
#         products = Product.objects.filter(status=True).order_by('-id').distinct()
#         print("All Products:", products)

#         if len(categories) > 0:
#             products = products.filter(category__cid__in=categories).distinct()
#             print("Filtered by Categories:", products)

#         # Apply additional filters, e.g., price range
#         products = products.filter(price__range=(min_price, max_price))
#         print("Filtered by Price Range:", products)

#         # Render the filtered products
#         data = render_to_string('app1/async/product-list.html', {"products": products})

#         return JsonResponse({"data": data})
#     except Exception as e:
#         return JsonResponse({"error": str(e)})


    
# ajax for variants
# def get_variant_details(request):
    # if request.method == 'GET':
    #     product_id = request.GET.get('product_id')
    #     variant_value = request.GET.get('variant')

    #     try:
    #         # Fetch variant-specific details from the database
    #         product = get_object_or_404(Product, pk=product_id)
    #         variant = Variants.objects.get(product=product, size=variant_value)  # Assuming size is the field in Variants model corresponding to the selected size

    #         # Customize the response data based on your model fields
    #         variant_details = {
    #             'price': str(variant.price),  # Convert to string if needed
    #             'stock_count': variant.stock_count,
    #             # Add other details as needed
    #         }

    #         return JsonResponse(variant_details)

    #     except Product.DoesNotExist:
    #         return JsonResponse({'error': 'Product not found'})

    #     except Variants.DoesNotExist:
    #         return JsonResponse({'error': 'Variant not found'})

    # return JsonResponse({'error': 'Invalid request method'})
    
    
    
        
    



def add_to_cart(request):
    cart_product = {
        str(request.GET['id']): {
            'title': request.GET['title'],
            'qty': request.GET['qty'],
            'price': request.GET['price'],
            'pid': request.GET['pid'],
            'image': request.GET['image'],
        }
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product

    return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})




# def cart_view(request):
    cart_total_amount =0
    if 'cart_data_obj' in request.session:
        for p_id,item in request.session['cart_data_obj'].items():
            cart_total_amount+= int(item['qty']) * float(item['price'])
        return render(request,'app1/cart.html',{"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount}) 
    else:
        messages.warning(request,"Your cart is empty")
        return redirect('app1:index')

def cart_view(request):
    cart_total_amount = 0

    if 'cart_data_obj' in request.session:
        cart_data = request.session.get('cart_data_obj', {})

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

        return render(request, 'app1/cart.html', {
            'cart_data': cart_data,
            'totalcartitems': len(cart_data),
            'cart_total_amount': cart_total_amount
        })
    else:
        messages.warning(request, "Your cart is empty")
        return redirect('app1:index')
    
    
    
# def delete_item_from_cart(request):
#     product_id = str(request.GET['id'])
#     if 'cart_data_obj' in request.session:
#         if product_id in request.session['cart_data_obj']:
#             cart_data = request.session['cart_data_obj']
#             del request.session['cart_data_obj'][product_id]
#             request.session['cart_data_obj']=cart_data
            
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
            
#     context=render_to_string("app1/async/cart-list.html",{
#             'cart_data': cart_data,
#             'totalcartitems': len(cart_data),
#             'cart_total_amount': cart_total_amount
#         })
#     return JsonResponse({"data":context,'totalcartitems': len(cart_data)})



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
    
        return render (request,'app1/checkout.html',{
        'cart_data': cart_data,
        'totalcartitems': len(cart_data),
        'cart_total_amount': cart_total_amount
    })
