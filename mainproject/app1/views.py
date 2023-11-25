from django.db.models import Count
from django.shortcuts import render
from app1.models import Product,ProductImages,Category
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator
from decimal import Decimal



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


def product_detail(request,pid):
    product = Product.objects.get(pid = pid)
    p_image =product.p_images.all()
    category = Category.objects.all()
    products = Product.objects.filter(category=product.category).exclude(pid=pid)[:4]
    
    
    context={
        "product":product,
        "p_image":p_image,
        "category":category,
        "products":products
        
        
        
    }
    return render (request,'app1/product_detail.html',context)

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
#     categories =request.GET.getlist('Category[]')
    
#     products =Product.objects.filter(status=True).order_by('-id').distinct()
    
#     if len(categories) > 0:
#         products=products.filter(category__id__in=categories).distinct()
        
#     data =render_to_string('app1/async/product-list.html',{"products":products})
#     return JsonResponse ({"data":data})
    
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


    
