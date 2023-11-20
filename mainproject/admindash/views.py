from django.shortcuts import render,redirect,get_object_or_404
from app1.models import Product,Category,ProductImages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from admindash.forms import CreateProductForm,ProductImagesForm
from django.http import HttpResponse,HttpResponseRedirect
from django.forms import inlineformset_factory



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
def admin_products_details(request, pid):
    print(pid)
    if not request.user.is_authenticated:
        return redirect('adminside:admin_login')

    try:
        product = Product.objects.get(pid=pid)
       
    except Product.DoesNotExist:
        return HttpResponse("Product not found", status=404)

    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # Save the form including the image
            product = form.save(commit=False)
            product.image = form.cleaned_data['new_image']
            product.save()
            
            return redirect('admindash:admin_products_list')
        else:
            print(form.errors)
            context = {
                'form': form,
                'product': product,
                
            }
            return render(request, 'adminside/admin_products_details.html', context)

    else:
        initial_data = {'new_image': product.image.url if product.image else ''}
        form = CreateProductForm(instance=product, initial=initial_data)
        # print(form)
    
    context = {
        'form': form,
        'product': product,
        
    }
    return render(request, 'adminside/admin_products_details.html', context)

# def admin_products_details(request, pid):
#     print(pid)
#     if not request.user.is_authenticated:
#         return redirect('adminside:admin_login')

#     try:
#         product = Product.objects.get(pid=pid)
#     except Product.DoesNotExist:
#         return HttpResponse("Product not found", status=404)

#     ProductImagesFormSet = inlineformset_factory(Product, ProductImages, form=ProductImagesForm)

#     if request.method == 'POST':
#         ProductImagesFormSet = inlineformset_factory(Product, ProductImages, form=ProductImagesForm)
#         product_form = CreateProductForm(request.POST, request.FILES, instance=product)
#         images_formset = ProductImagesFormSet(request.POST, request.FILES, instance=product)

#         if product_form.is_valid() and images_formset.is_valid():
#             product = product_form.save(commit=False)
#             product.image = product_form.cleaned_data['new_image']
#             product.save()

#             images_formset.save()

#             return redirect('admindash:admin_products_list')
#         else:
#             print(product_form.errors)
#             print(images_formset.errors)

#             context = {
#                 'product_form': product_form,
#                 'images_formset': images_formset,
#                 'product': product,
#             }

#             return render(request, 'adminside/admin_products_details.html', context)

#     else:
#         initial_data = {'new_image': product.image.url if product.image else ''}
#         product_form = CreateProductForm(instance=product, initial=initial_data)
#         images_formset = ProductImagesFormSet(instance=product)

#     context = {
#         'product_form': product_form,
#         'images_formset': images_formset,
#         'product': product,
#     }

#     return render(request, 'adminside/admin_products_details.html', context)






  
@login_required(login_url='adminside:admin_login')
  
def block_unblock_products(request, pid):
  if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
  product = get_object_or_404(Product, pid=pid)
  if product.status:
    product.status=False
  else:
      product.status=True
  product.save()
  return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
  
    
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_product(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    categories = Category.objects.all()
   

    if request.method == 'POST':
        product_name= request.POST.get('title')
        # product_sk_id= request.POST.get('sku')
        description= request.POST.get('description')
        max_price= request.POST.get('old_price')
        sale_price= request.POST.get('price')
        category_name= request.POST.get('category')
       
       

        category = get_object_or_404(Category, title=category_name)
        

        product = Product(
            title=product_name,
            # sku=product_sk_id,
            category=category,
            
            description=description,
            old_price=max_price,
            price=sale_price,
            image=request.FILES['image_feild']  # Make sure your file input field is named 'product_image'
        )
        product.save()

        return redirect('admindash:admin_products_list')
    else:
        form=CreateProductForm()
    content = {
        'categories': categories,
          
        'form': form
    }
    return render(request,'adminside/admin_add_product.html', content)





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_product(request,pid):
    if not request.user.is_authenticated:
        return redirect('adminside:admin_login')
    try:
        product = Product.objects.get(pid=pid)
        product.delete()
        return redirect('admindash:admin_products_list')
    except Product.DoesNotExist:
        return HttpResponse("Product not found", status=404)
    
    
    
    
def admin_category_list(request):
    if not request.user.is_authenticated:
        return redirect('adminside:admin_login')
    
    categories = Category.objects.all()
    
    context = {
        'categories':categories
    }
    
    return render(request,'adminside/admin_category_list.html',context)

def admin_add_category(request):
    if request.method == 'POST':
        cat_title = request.POST.get('category_name')
        
        cat_data = Category(title=cat_title,
                            image=request.FILES.get('category_image'))
    
        cat_data.save()
    else:
        return render(request, 'adminside/admin_category_list.html')
    
    return render(request, 'adminside/admin_category_list.html')

    
    
    
    
    

    
        
        
        
    
        
    
    


  