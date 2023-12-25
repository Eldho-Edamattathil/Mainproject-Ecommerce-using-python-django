from django.shortcuts import render,redirect,get_object_or_404
from app1.models import Product,Category,ProductImages,Coupon,wallet,ProductOffer,CategoryOffer
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from admindash.forms import CreateProductForm,ProductImagesForm,CouponForm
from django.http import HttpResponse,HttpResponseRedirect
from django.forms import inlineformset_factory
from django.contrib import messages
from django.core.paginator import Paginator
from app1.models import CartOrder,CartOrderItems
import calendar
from django.db.models.functions import ExtractMonth
from django.db.models import Count,Avg
from decimal import Decimal
from app1.forms import ProductOfferForm,CategoryOfferForm
from datetime import datetime,timedelta
from django.utils import timezone
from django.utils.timezone import make_aware
from userauths.models import User
from django.db.models.functions import TruncMonth, TruncYear


@login_required(login_url='adminside:admin_login')  # Use the named URL pattern
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    # if not request.user.is_authenticated:
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')

    product_count=Product.objects.count()
    category_count=Category.objects.count()
    # orders= CartOrder.objects.annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month","count")
    # month=[]
    # total_orders=[]
    # for i in orders:
    #     month.append(calendar.month_name[i["month"]])
    #     total_orders.append(i["count"])
    
    orders = CartOrder.objects.all()
    last_orders = CartOrder.objects.order_by('-order_date')[:5]
    orders_count = orders.count()
    total_users_count = User.objects.count()
    total = 0

    for order in orders:
        if order.product_status == 'Delivered':
            total += order.price  
        if order.paid_status:
            total += order.price  
    revenue=int(total)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    daily_order_counts = (
        CartOrder.objects
        .filter(order_date__range=(start_date, end_date), paid_status=True)
        .values('order_date')
        .annotate(order_count=Count('id'))
        .order_by('order_date')
    )

    dates = [entry['order_date'].strftime('%Y-%m-%d') for entry in daily_order_counts]
    counts = [entry['order_count'] for entry in daily_order_counts]
   
    
    monthly_order_counts = (
        CartOrder.objects
        .filter(order_date__year=datetime.now().year, paid_status=True)  # Filter by current year and paid orders
        .annotate(month=TruncMonth('order_date'))
        .values('month')
        .annotate(order_count=Count('id'))
        .order_by('month')
    )

    monthly_dates = [entry['month'].strftime('%Y-%m') for entry in monthly_order_counts]
    monthly_counts = [entry['order_count'] for entry in monthly_order_counts]

    # Fetch yearly order counts and their respective dates
    yearly_order_counts = (
        CartOrder.objects
        .annotate(year=TruncYear('order_date'))
        .values('year')
        .annotate(order_count=Count('id'))
        .order_by('year')
    )

    yearly_dates = [entry['year'].strftime('%Y') for entry in yearly_order_counts]
    yearly_counts = [entry['order_count'] for entry in yearly_order_counts]

    # statuses = ['Delivered', 'Processing', 'Cancelled', 'Return','Shipped']
    # order_counts = [CartOrder.objects.filter(product_status=status).count() for status in statuses]
    statuses = ['Delivered', 'Processing', 'Cancelled', 'Return', 'Shipped']

    order_counts = (
        CartOrder.objects
        .filter(product_status__in=statuses)
        .values('product_status')
        .annotate(count=Count('id'))
        .order_by('product_status')
    )
    status_list = [entry['product_status'] for entry in order_counts]
    count_list = [entry['count'] for entry in order_counts]

    
    context={
        'product_count':product_count,
        'category_count':category_count,
        'orders_count':orders_count,
        'dates':dates,
        'counts':counts,
        'monthlyDates':monthly_dates,
        'monthlyCounts':monthly_counts,
        'yearlyDates':yearly_dates,
        'yearlyCounts':yearly_counts,
        'last_orders':last_orders,
        'revenue':revenue,
        'total_users_count':total_users_count,
        'status_list':status_list,
        'count_list':count_list
        
        
        
        
    }

    return render(request, 'adminside/admin_index.html', context)
  
  
def admin_products_list(request):
  
  products = Product.objects.all()
  p=Paginator(Product.objects.all(),10)
  page=request.GET.get('page')
  productss=p.get_page(page)
  
  context ={
    "products":products ,
    "productss":productss
  }
  return render(request,'adminside/admin_products_list.html', context)





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def admin_products_details(request, pid):
#     print(pid)
#     if not request.user.is_authenticated:
#         return redirect('adminside:admin_login')

#     try:
#         product = Product.objects.get(pid=pid)
       
#     except Product.DoesNotExist:
#         return HttpResponse("Product not found", status=404)

#     if request.method == 'POST':
#         form = CreateProductForm(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             # Save the form including the image
#             product = form.save(commit=False)
#             product_image = form.cleaned_data['new_image']
#             if product_image is not None:
#                 product.image=product_image
            
#             product.save()
            
#             return redirect('admindash:admin_products_list')
#         else:
#             print(form.errors)
#             context = {
#                 'form': form,
#                 'product': product,
                
#             }
#             return render(request, 'adminside/admin_products_details.html', context)

#     else:
#         initial_data = {'new_image': product.image.url if product.image else ''}
#         form = CreateProductForm(instance=product, initial=initial_data)
#         # print(form)
    
#     context = {
#         'form': form,
#         'product': product,
        
#     }
#     return render(request, 'adminside/admin_products_details.html', context)



@login_required(login_url='adminside:admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_products_details(request, pid):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    # if not request.user.is_superadmin:
    #     return redirect('adminside:admin_login')

    try:
        product = Product.objects.get(pid=pid)
        product_images = ProductImages.objects.filter(product=product)
    except Product.DoesNotExist:
        return HttpResponse("Product not found", status=404)

    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # Save the form including the image
            product = form.save(commit=False)
            product_image = form.cleaned_data['new_image']
            if product_image is not None:
                product.image = product_image
            product.save()

            # Update or create additional images
            for i in product_images:
                image_field_name = f'product_image{i.id}'
                image = request.FILES.get(image_field_name)

                if image:
                    i.Images = image
                    i.save()

            return redirect('admindash:admin_products_list')
        else:
            print(form.errors)
            context = {
                'form': form,
                'product': product,
                'product_images': product_images,
            }
            return render(request, 'adminside/admin_products_details.html', context)
    else:
        initial_data = {'new_image': product.image.url if product.image else ''}
        form = CreateProductForm(instance=product, initial=initial_data)

    context = {
        'form': form,
        'product': product,
        'product_images': product_images,
    }
    return render(request, 'adminside/admin_products_details.html', context)

















  

@login_required(login_url='adminside:admin_login') 
def block_unblock_products(request, pid):
    
  if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
  product = get_object_or_404(Product, pid=pid)
  if product.status:
    product.status=False
  else:
      product.status=True
  product.save()
  return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
  
    
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def add_product(request):
#     if not request.user.is_authenticated:
#         return HttpResponse("Unauthorized", status=401)
#     categories = Category.objects.all()
   

#     if request.method == 'POST':
#         product_name= request.POST.get('title')
#         product_stock_count= request.POST.get('stock_count')
#         description= request.POST.get('description')
#         max_price= request.POST.get('old_price')
#         sale_price= request.POST.get('price')
#         category_name= request.POST.get('category')
        
       
       

#         category = get_object_or_404(Category, title=category_name)
        

#         product = Product(
#             title=product_name,
#             stock_count=product_stock_count,
#             category=category,
            
#             description=description,
#             old_price=max_price,
#             price=sale_price,
#             image=request.FILES['image_feild']  # Make sure your file input field is named 'product_image'
#         )
#         product.save()
        

#         return redirect('admindash:admin_products_list')
#     else:
#         form=CreateProductForm()
#     content = {
#         'categories': categories,
          
#         'form': form
#     }
#     return render(request,'adminside/admin_add_product.html', content)


# new add produt


@login_required(login_url='adminside:admin_login')
def add_product(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)

    categories = Category.objects.all()

    if request.method == 'POST':
        product_name = request.POST.get('title')
        product_stock_count = request.POST.get('stock_count')
        description = request.POST.get('description')
        max_price = request.POST.get('old_price')
        sale_price = request.POST.get('price')
        category_name = request.POST.get('category')
        # validations
        validation_errors = []

        try:
            product_stock_count = int(product_stock_count)
            if product_stock_count < 0:
                validation_errors.append("Stock Count must be a non-negative integer.")

            max_price = float(max_price)
            if max_price < 0:
                validation_errors.append("Max Price must be a non-negative number.")

            sale_price = float(sale_price)
            if sale_price < 0:
                validation_errors.append("Sale Price must be a non-negative number.")
        except ValueError as e:
            validation_errors.append(str(e))

        if validation_errors:
            form_data = {
                'title': product_name,
                'stock_count': product_stock_count,
                'description': description,
                'old_price': max_price,
                'price': sale_price,
                'category': category_name,
            }
            form = CreateProductForm()
            content = {
                'categories': categories,
                'form': form,
                'additional_image_count': range(1, 4),
                'error_messages': validation_errors,
                'form_data': form_data,
            }
            return render(request, 'adminside/admin_add_product.html', content)
        
        # till here
        

        category = get_object_or_404(Category, title=category_name)

        product = Product(
            title=product_name,
            stock_count=product_stock_count,
            category=category,
            description=description,
            old_price=max_price,
            price=sale_price,
            image=request.FILES['image_feild']
        )
        product.save()

        # Handling additional images
        additional_image_count = 5  # Change this to the desired count of additional images
        for i in range(1, additional_image_count + 1):
            image_field_name = f'product_image{i}'
            image = request.FILES.get(image_field_name)
            if image:
                ProductImages.objects.create(product=product, Images=image)

        return redirect('admindash:admin_products_list')
    else:
        form = CreateProductForm()
        form_data = {
            'title': '',
            'stock_count': '',
            'description': '',
            'old_price': '',
            'price': '',
            'category': '',
        }

    content = {
        'categories': categories,
        'form': form,
         'additional_image_count': range(1, 4), 
         'form_data': form_data,
    }
    return render(request, 'adminside/admin_add_product.html', content)


#ends here

@login_required(login_url='adminside:admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_product(request,pid):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    try:
        product = Product.objects.get(pid=pid)
        product.delete()
        return redirect('admindash:admin_products_list')
    except Product.DoesNotExist:
        return HttpResponse("Product not found", status=404)
    
    
    
@login_required(login_url='adminside:admin_login')  
def admin_category_list(request):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    
    categories = Category.objects.all()
    
    context = {
        'categories':categories
    }
    
    return render(request,'adminside/admin_category_list.html',context)


@login_required(login_url='adminside:admin_login')
def admin_add_category(request):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    if request.method == 'POST':
        cat_title = request.POST.get('category_name')
        if Category.objects.filter(title=cat_title).exists():
            messages.error(request, 'Category with this title already exists.')
        else:
            cat_data = Category(title=cat_title, image=request.FILES.get('category_image'))
            cat_data.save()
            messages.success(request, 'Category added successfully.')
        
        
        # cat_data = Category(title=cat_title,
        #                     image=request.FILES.get('category_image'))
    
        # cat_data.save()
    else:
        return render(request, 'adminside/admin_category_list.html')
    
    return render(request, 'adminside/admin_category_list.html')




# def admin_category_edit(request, cid):
    if not request.user.is_authenticated:
        return redirect('adminside:admin_login')

    # Using get_object_or_404 to get the Category or return a 404 response if it doesn't exist
    categories = get_object_or_404(Category, cid=cid)
    categories_title=categories.title
    categories_image=categories.image
    
    context={
        'categories_title':categories_title,
        'categories_image':categories_image
    }

    if request.method == 'POST':
        # Update the fields of the existing category object
        cat_title = request.POST.get("category_name")
        cat_image = request.FILES.get('category_image')
        categories_title=cat_title
        categories_image=cat_image
        
        categories.save()
        

        # Save the changes to the database
        return redirect('admindash:admin_category_list')
    
   
        

    # context = {
    #     "categories": categories
    # }

    # Render the template even for GET requests to display the form
    return render(request, 'adminside/admin_category_edit.html', context)
@login_required(login_url='adminside:admin_login')
def admin_category_edit(request, cid):
    if not request.user.is_authenticated:
        return redirect('adminside:admin_login')

    # Using get_object_or_404 to get the Category or return a 404 response if it doesn't exist
    categories = get_object_or_404(Category, cid=cid)

    if request.method == 'POST':
        # Update the fields of the existing category object
        cat_title = request.POST.get("category_name")
        cat_image = request.FILES.get('category_image')

        # Update the category object with the new title and image
        categories.title = cat_title
        if cat_image is not None:
            categories.image = cat_image

        
        # Save the changes to the database
        categories.save()

        # Redirect to the category list page after successful update
        return redirect('admindash:admin_category_list')

    # If the request method is GET, render the template with the category details
    context = {
        "categories_title": categories.title,
        "categories_image": categories.image,
    }

    return render(request, 'adminside/admin_category_edit.html', context)



@login_required(login_url='adminside:admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_category(request,cid):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    try:
        category=Category.objects.get(cid=cid)
    except ValueError:
        return redirect('admindash:admin_category_list')
    category.delete()

    return redirect('admindash:admin_category_list')


@login_required(login_url='adminside:admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def available_category(request,cid):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    
    category = get_object_or_404(Category, cid=cid)
    
    if category.is_blocked:
        category.is_blocked=False
       
    else:
        category.is_blocked=True
    category.save()

    
    # cat_list=Category.objects.filter(parent_id=category_id)
    # for i in cat_list.values():
    #     print(i)
    
    # for category in cat_list:
    #     if category.is_available:
    #         category.is_available=False
    #     else:
    #         category.is_available=True
    #     category.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))







# order management
@login_required(login_url='adminside:admin_login')
def order_list(request):
    if not request.user.is_authenticated and not request.user.is_superadmin:
        
        return redirect('adminside:admin_login')
    order=CartOrder.objects.all().order_by("-id")
    p=Paginator(CartOrder.objects.all().order_by("-id"),10)
    page=request.GET.get('page')
    orders=p.get_page(page)
    

    context = {
        'order': order,
        'orders':order
       
    }
    
        
    
    
    return render(request, 'adminside/order-list.html',{
        'order':order,'orders':orders
    })
    
    
    
@login_required(login_url='adminside:admin_login')   
def update_product_status(request, id):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    if request.method == 'POST':
        new_status = request.POST.get('product_status')
        order = get_object_or_404(CartOrder, id=id)
        order.product_status = new_status
        order.save()
        
        products = CartOrderItems.objects.filter(order=order)
        for p in products:
            productss = Product.objects.filter(title=p.item)
            for s in productss:
                s.stock_count = int(s.stock_count) + p.qty
                s.save()

    # Redirect back to the original page or a specific URL
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    
def admin_order_detail(request,id):
    order = get_object_or_404(CartOrder, id=id)
    print(order)

    # Use filter based on the specific order instance
    products = CartOrderItems.objects.filter(order=order)

    context = {
        'products': products,
        'order': order,
    }
    
    return render(request,'adminside/admin-order-detail.html',context)





    
    
# admin cancel order

# def admin_cancel_order(request,id):
#     order = get_object_or_404(CartOrder, id=id)
#     print(order)
#     order.product_status='cancelled'
#     order.save()
#     products = CartOrderItems.objects.filter(order=order)
#     for p in products:
#         print(p.item)
#         productss=Product.objects.filter(title=p.item)
#         for s in productss:
#             print(s.stock_count)
#             s.stock_count = int(s.stock_count)+p.qty
#             s.save()
            
            
            
    
    
    
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    

    
@login_required(login_url='adminside:admin_login')      
def admin_cancel_order(request, id):
    # if not request.user.is_superadmin:
    #     return redirect('adminside:admin_login')
    order = get_object_or_404(CartOrder, id=id)
    # user_wallet = get_object_or_404(wallet, user=request.user)
    user_wallet, created = wallet.objects.get_or_create(user=request.user)

    if order.product_status == 'cancelled':
        messages.warning(request, f"Order {order.id} is already cancelled.")
    else:
        # Update order status to 'cancelled'
        order.product_status = 'cancelled'
        order.wallet_status=True
        order.save()
        
        if order.paid_status==True:
            user_wallet.Amount+=order.price
            # credit=order.price
            # request.session['credit']=credit
            user_wallet.save()
            messages.warning(request,"Refund amount has been added to the wallet")
            

        # Update product stock count
        products = CartOrderItems.objects.filter(order=order)
        for p in products:
            productss = Product.objects.filter(title=p.item)
            for s in productss:
                s.stock_count = int(s.stock_count) + p.qty
                s.save()

        messages.success(request, f"Order {order.id} has been cancelled successfully.")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))    


@login_required(login_url='adminside:admin_login')
def admin_coupon(request):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    coupon=Coupon.objects.all()
    
    
    context={
        'coupon':coupon
    }
    return render(request,'adminside/admin-coupon.html',context)

@login_required(login_url='adminside:admin_login')
def create_coupon(request):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    if request.method == 'POST':
        code = request.POST['code']
        discount = request.POST['discount']
        active = request.POST.get('active') == 'on'
        active_date = request.POST['active_date']
        expiry_date = request.POST['expiry_date']

        # Check if active_date is not greater than expiry_date
        if active_date > expiry_date:
            messages.error(request, 'Active date should not be greater than expiry date')
            return render(request, 'adminside/create-coupon.html')

        # Check if the coupon with the same code already exists
        if Coupon.objects.filter(code=code).exists():
            messages.error(request, f'Coupon with code {code} already exists')
            return render(request, 'adminside/create-coupon.html')

        coupon = Coupon(
            code=code,
            discount=discount,
            active=active,
            active_date=active_date,
            expiry_date=expiry_date
        )
        coupon.save()
        messages.success(request, 'Coupon created successfully')
        return redirect('admindash:admin-coupon')

    return render(request, 'adminside/create-coupon.html')


@login_required(login_url='adminside:admin_login')
def edit_coupon(request,id):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    
    coupon_code = get_object_or_404(Coupon, id=id)
    print(f'Active Date: {coupon_code.active_date}')
    if request.method == 'POST':
        code = request.POST['code']
        discount = request.POST['discount']
        active = request.POST.get('active') == 'on'
        active_date = request.POST['active_date']
        expiry_date = request.POST['expiry_date']
        

        # Check if active_date is not greater than expiry_date
        if active_date > expiry_date:
            messages.error(request, 'Active date should not be greater than expiry date')
            return render(request, 'adminside/create-coupon.html')
        
        coupon_code.code=code
        coupon_code.discount=discount
        coupon_code.active_date=active_date
        coupon_code.expiry_date=expiry_date
        coupon_code.active=active
        coupon_code.save()
        messages.success(request, 'Coupon Updated successfully')
        return redirect('admindash:admin-coupon')
    
        
    
    return render (request, 'adminside/edit-coupon.html',{'coupon_code':coupon_code})


@login_required(login_url='adminside:admin_login')        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_coupon(request,id):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    
    try:
        coupon= get_object_or_404(Coupon, id=id)
    except ValueError:
        return redirect('admindash:admin-coupon')
    coupon.delete()
    messages.warning(request,"Coupon has been deleted successfully")

    return redirect('admindash:admin-coupon')
    


  
  


def product_offers(request):
    offers=ProductOffer.objects.all()
    try:
        product_offer = ProductOffer.objects.get(active=True)
        print(product_offer)
    except ProductOffer.DoesNotExist:
       
        product_offer = None
    
    products = Product.objects.all()

    for p in products:
       
        if product_offer:
           
            discounted_price = p.old_price - (p.old_price * product_offer.discount_percentage / 100)
            p.price = max(discounted_price, Decimal('0.00'))  # Ensure the price is not negative
        else:
            
            p.price = p.old_price

        p.save()

    
    context={
        'offers':offers
    }
    return render(request, 'adminside/product_offers.html',context)



def edit_product_offers(request, id):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    
    offer_discount = get_object_or_404(ProductOffer, id=id)
    print(f'Active Date: {offer_discount.start_date}')

    if request.method == 'POST':
        discount = request.POST['discount']
        active = request.POST.get('active') == 'on'
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        
        if end_date and start_date and end_date < start_date:
            messages.error(request, 'Expiry date must not be less than the start date.')
        else:
            start_date = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
            end_date = make_aware(datetime.strptime(end_date, '%Y-%m-%d'))

            current_date = timezone.now()
            if start_date and end_date and (current_date < start_date or current_date > end_date):
                active = False
                messages.error(request, 'Offer cannot be activated now. Check the start date.')
           
            active_category_offer = CategoryOffer.objects.filter(active=True).first()

            if active_category_offer:
               
                messages.error(request, 'Cannot create/update product offer when a category offer is active.')
                return redirect('admindash:product-offers')

           
            if active:
                ProductOffer.objects.exclude(id=offer_discount.id).update(active=False)

            offer_discount.discount_percentage = discount or None
            offer_discount.start_date = start_date or None
            offer_discount.end_date = end_date or None
            offer_discount.active = active
            offer_discount.save()

            messages.success(request, 'Offer Updated successfully')
            return redirect('admindash:product-offers')
    
    return render(request, 'adminside/edit_product_offers.html', {'offer_discount': offer_discount})
        
            



def create_product_offer(request):
    if request.method == 'POST':
        form = ProductOfferForm(request.POST)
        if form.is_valid():
            discount_percentage = form.cleaned_data['discount_percentage']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            active = form.cleaned_data['active']
            
            if end_date and start_date and end_date < start_date:
                messages.error(request, 'Expiry date must not be less than the start date.')
            else:
                
                current_date = timezone.now()
                if start_date and end_date and (current_date < start_date or current_date > end_date):
                    active = False
                    messages.error(request, 'Offer cannot be activated now. Check the start date.')

                if active:
                    ProductOffer.objects.update(active=False)

            # Check if any of the fields are filled
                if discount_percentage or start_date or end_date or active:
               
                    form.save()
            
            return redirect('admindash:product-offers')  # Redirect to a view displaying the list of product offers
    else:
        form = ProductOfferForm()

    return render(request, 'adminside/create-product-offers.html', {'form': form})


@login_required(login_url='adminside:admin_login')        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_product_offer(request,id):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    
    try:
        offer= get_object_or_404(ProductOffer, id=id)
    except ValueError:
        return redirect('admindash:product-offers')
    offer.delete()
    messages.warning(request,"Offer has been deleted successfully")

    return redirect('admindash:product-offers')




# Category Offers





def category_offers(request):
    offers = CategoryOffer.objects.all()
    categories = Category.objects.all()

    for category in categories:
        try:
            category_offer = CategoryOffer.objects.filter(category=category, active=True)
            print(category_offer)
        except CategoryOffer.DoesNotExist:
            category_offer = None
        products = Product.objects.filter(category=category, status=True)
        print(products)
        
        for product in products:
            if category_offer:
                for cat in category_offer:
            

            
                    discounted_price = product.old_price - (product.old_price * cat.discount_percentage / 100)
                    product.price = max(discounted_price, Decimal('0.00'))  # Ensure the price is not negative
                
            else:
                product.price=product.old_price
            product.save()
                

    context = {
        'offers': offers
    }
    return render(request, 'adminside/category_offers.html', context)








# def edit_category_offers(request, id):
#     if not request.user.is_superadmin:
#         return redirect('adminside:admin_login')

#     offer_discount = get_object_or_404(CategoryOffer, id=id)
#     print(f'Active Date: {offer_discount.start_date}')

#     if request.method == 'POST':
#         discount = request.POST.get('discount')
        
#         active = request.POST.get('active') == 'on'
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')

#         if end_date and start_date:
#             end_date = datetime.strptime(end_date, '%Y-%m-%d')
#             start_date = datetime.strptime(start_date, '%Y-%m-%d')
#             if end_date < start_date:
#                 messages.error(request, 'Expiry date must not be less than the start date.')
#                 return redirect('admindash:edit-category-offers', id=id)

        
#         offer_discount.discount_percentage = discount or None
       
#         offer_discount.start_date = start_date or None
#         offer_discount.end_date = end_date or None
#         offer_discount.active = active
#         offer_discount.save()

#         messages.success(request, 'Offer updated successfully')
#         return redirect('admindash:category-offers')

#     return render(request, 'adminside/edit_category_offers.html', {'offer_discount': offer_discount})



def edit_category_offers(request, id):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')

    offer_discount = get_object_or_404(CategoryOffer, id=id)
    print(f'Active Date: {offer_discount.start_date}')

    if request.method == 'POST':
        discount = request.POST.get('discount')
        active = request.POST.get('active') == 'on'
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if end_date and start_date:
            end_date = make_aware(datetime.strptime(end_date, '%Y-%m-%d'))
            start_date = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))

            if end_date < start_date:
                messages.error(request, 'Expiry date must not be less than the start date.')
                return redirect('admindash:edit-category-offers', id=id)

            # Check if the offer can be activated based on the current date
            current_date = timezone.now()
            if start_date and end_date and (current_date < start_date or current_date > end_date):
                active = False
                messages.error(request, 'Offer cannot be activated now. Check the start date.')
            
       

        # Check if there's an active product offer
        active_product_offer = ProductOffer.objects.filter(active=True).first()

        if active_product_offer:
            
            messages.error(request, 'Cannot activate category offer when a product offer is active.')
            return redirect('admindash:category-offers')
        
        if active:
            CategoryOffer.objects.exclude(id=offer_discount.id).update(active=False)

        # Continue with your existing logic to update the category offer
        offer_discount.discount_percentage = discount or None
        offer_discount.start_date = start_date or None
        offer_discount.end_date = end_date or None
        offer_discount.active = active
        offer_discount.save()

        messages.success(request, 'Offer updated successfully')
        return redirect('admindash:category-offers')

    return render(request, 'adminside/edit_category_offers.html', {'offer_discount': offer_discount})



def create_category_offer(request):
    if request.method == 'POST':
        form = CategoryOfferForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            discount_percentage = form.cleaned_data['discount_percentage']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            active = form.cleaned_data['active']

            if end_date and start_date and end_date < start_date:
                messages.error(request, 'Expiry date must not be less than the start date.')
            else:
                # Check if there is an active offer for the selected category
                if active and CategoryOffer.objects.filter(category=category, active=True).exists():
                    messages.error(request, 'An active offer already exists for this category.')
                   
                else:
                    current_date = timezone.now()
                    if start_date and end_date and (current_date < start_date or current_date > end_date):
                        active = False
                        messages.error(request, 'Offer cannot be activated now. Check on start date')
                    
                    if active:
                        CategoryOffer.objects.update(active=False)
                    if discount_percentage or start_date or end_date or active:
                        form.save()

                    return redirect('admindash:category-offers')  
    else:
        form = CategoryOfferForm()

    return render(request, 'adminside/create_category_offer.html', {'form': form})



@login_required(login_url='adminside:admin_login')        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_category_offer(request,id):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    
    try:
        offer= get_object_or_404(CategoryOffer, id=id)
    except ValueError:
        return redirect('admindash:category-offers')
    offer.delete()
    messages.warning(request,"Offer has been deleted successfully")

    return redirect('admindash:category-offers')




                    
                   
                    