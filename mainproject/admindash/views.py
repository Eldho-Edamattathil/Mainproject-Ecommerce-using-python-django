from django.shortcuts import render,redirect
from app1.models import Product,Category
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from admindash.forms import CreateProductForm
from django.http import HttpResponse



@login_required(login_url='adminside:admin_login')  # Use the named URL pattern
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('admindash:admin_login')

    product_count=Product.objects.count()
    category_count=Category.objects.count()
    
    context={
        'product_count':product_count,
        'category_count':category_count
    }

    return render(request, 'adminside/admin_index.html', context)
  
  
def admin_products_list(request):
  
  products = Product.objects.all()
  context ={
    "products":products 
  }
  return render(request,'adminside/admin_products_list.html', context)





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_products_details(request, product_id):
    print(product_id)
    if not request.user.is_authenticated:
        return redirect('adminlog:admin_login')

    try:
        product = Product.objects.get(pid=product_id)
       
    except Product.DoesNotExist:
        return HttpResponse("Product not found", status=404)

    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admindash:admin_products_list')
        else:
            print(form.errors)
            context = {
                'form': form,
                'product': product,
                
            }
            return render(request, 'adminside/admin_products_details.html', context)

    else:
        form = CreateProductForm(instance=product)
        # print(form)
    context = {
        'form': form,
        'product': product,
        
    }
    return render(request, 'adminside/admin_products_details.html', context)


  