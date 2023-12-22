from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from userauths.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
# Create your views here.




def admin_login(request):
    if request.user.is_authenticated:
        if request.user.is_superadmin:
            return redirect('admindash:dashboard')
    
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        print(email,password)
        user = authenticate(request, email=email, password=password)
        print(user)
        if user:
            if  user.is_superadmin:
                login(request, user)
                # messages.success(request, "Admin login successful!")
                return redirect('admindash:dashboard')  # Use the named URL pattern

            messages.error(request, "Invalid admin credentials!")
    return render(request, 'adminside/admin_login.html')


def admin_logout(request):
    logout(request)

    return redirect('adminside:admin_login')
  
  
@login_required(login_url='adminside:admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def users_list(request):
    if not request.user.is_authenticated:
        return redirect('adminside:admin_login')
    
    search_query=request.GET.get('query')

    if search_query:
         users = User.objects.filter(username__icontains=search_query)
    else:
         users = User.objects.all().order_by('id')
         print("the users are :", users)
    context = {
        'users': users
    }
      
    return render(request,'adminside/users_list.html',context)
  
  
  
  
@login_required(login_url='adminside:admin_login')
def block_unblock_user(request,user_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    
    user = get_object_or_404(User, id=user_id)
    
    if user.is_active:
        
        user.is_active=False
        
    else:
        user.is_active=True
        
    user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))