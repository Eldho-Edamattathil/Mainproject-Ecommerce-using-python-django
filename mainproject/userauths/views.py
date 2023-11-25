from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from app1.backends import EmailBackend  # Import your custom authentication backend
import random
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect,HttpResponseBadRequest
from django.urls import reverse


from userauths.models import User  # Import your custom user model



@never_cache
def register_view(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password=form.cleaned_data.get('password1')
            request.session["username"]=username
            request.session["password"]=password
            request.session["email"]=email
            messages.success(request, f'Hey {username}, Your account was created succesfully')
            email=request.POST["email"]
            send_otp(request)
            return render(request,'userauths/otp.html',{"email":email})
            
           
    else:
        form = CreateUserForm()

    context = {'form': form}
    return render(request, 'userauths/signup.html', context)


#OTP
@never_cache
def send_otp(request):
    s=""
    for x in range(0,4):
        s+=str(random.randint(0,9))
    request.session["otp"]=s
    send_mail("otp for sign up",s,'djangoalerts0011@gmail.com',[request.session['email']],fail_silently=False)
    return render(request,"userauths/otp.html")

@never_cache
def  otp_verification(request):
    if  request.method=='POST':
       
        otp_=request.POST.get("otp")
    if otp_ == request.session["otp"]:
        encryptedpassword=make_password(request.session['password'])
        nameuser=User(username=request.session['username'],email=request.session['email'],password=encryptedpassword)
        nameuser.save()
        messages.info(request,'signed in successfully...')
        User.is_active=True
       
        return redirect('app1:index')
    else:
        messages.error(request,"otp doesn't match")
        return render(request,'userauths/otp.html')
    
    
    
    
    
    
@never_cache
def login_view(request):
  
    if request.user.is_authenticated:
      messages.warning(request,f"Hey You are already logged in")
      return redirect("app1:index")
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        request.session["email"]=email
        print(email,password)
        if not User.objects.filter(email=email).exists():
            messages.error(request, "Invalid Email Adress")
            return redirect('userauths:login')
        
        if not User.objects.filter(email=email,is_active=True).exists():
            messages.error(request, "Account blocked ! ! !")
            return redirect('userauths:login') 
        try:
          user = User.objects.get(email=email)
          user = authenticate(email=email, password=password,backend = EmailBackend)
        

          if user is not None:
              login(request, user)
           
              messages.success(request, 'Login successful.')
              return redirect("app1:index")  # Redirect to the desired page after successful login
          else:
              messages.warning(request, 'Username or Password is incorrect.')

        except:
          messages.warning(request, f'User with {email} doesnot exists')
          
        
    context = {}
    return render(request, 'userauths/login.html', context)



@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_otp(request):
    
    if request.user.is_authenticated:
      messages.warning(request,f"Hey You are already logged in")
      return redirect("app1:index")
    if request.method == 'POST':
        email = request.POST.get('email')
        
        request.session["email"]=email
        print(email)
        if not User.objects.filter(email=email).exists():
            messages.error(request, "Invalid Email Adress")
            return redirect('userauths:login_otp')
        
        if not User.objects.filter(email=email,is_active=True).exists():
            messages.error(request, "Account blocked ! ! !")
            return redirect('userauths:login_otp') 
        try:
          user = User.objects.get(email=email)
        #   user = authenticate(email=email)
        

          if user is not None:
            send_otp_login(request)
            return render(request,'userauths/otp_login.html',{"email":email})
        #   
        except:
          messages.warning(request, f'User with {email} doesnot exists')
          

        # #   context = {'form': form}
        #   return render(request, 'userauths/login_otp')
              
        #       login(request, user)
        #       request.session['logged_in'] = True  # Set a session variable if needed
        #     messages.success(request, 'Login successful.')
        #     return redirect("app1:index")  # Redirect to the desired page after successful login
        #   else:
        #       messages.warning(request, 'Username or Password is incorrect.')

    return render(request,'userauths/login_otp.html')
    
    



# login _otp views
@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def send_otp_login(request):
    s=""
    for x in range(0,4):
        s+=str(random.randint(0,9))
    request.session["otp"]=s
    send_mail("otp for sign up",s,'djangoalerts0011@gmail.com',[request.session['email']],fail_silently=False)
    return render(request,"userauths/otp_login.html")


# @never_cache
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def  otp_verification_login(request):
#     if  request.method=='POST':
#         otp_=request.POST.get("otp")
#     if otp_ == request.session["otp"]:
#         # encryptedpassword=make_password(request.session['password'])
#         # nameuser=User(email=request.session['email'])
#         # nameuser.save()
#         messages.info(request,'signed in successfully...')
#         User.is_active=True
       
#         return redirect('app1:index')
#         request.session.pop('otp', None)
#     else:
#         messages.error(request,"otp doesn't match")
#         return render(request,'userauths/otp_login.html')
    
    
@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def otp_verification_login(request):
    if request.method == 'POST':
        otp_ = request.POST.get("otp")
        try:
            if otp_ == request.session["otp"]:
                # Clear the 'otp' session key after successful verification
                request.session.pop('otp', None)

                # Retrieve the user instance from the database
                user = User.objects.get(email=request.session.get("email"))

                # Set the user as active
                user.is_active = True
                
                user.save()
                

                messages.success(request, 'Account activated successfully.')
                redirect_url = reverse('app1:index')
                return HttpResponseRedirect(redirect_url)  # Replace '/app1/index' with your actual URL
            else:
                messages.error(request, "OTP doesn't match")
                return render(request, 'userauths/otp_login.html')
        except KeyError:
            messages.error(request, 'Session expired. Please try logging in again.')

    return HttpResponseBadRequest("Invalid request method")
    


# ends here
    




    
    
@never_cache
def logoutUser(request):
    logout(request)
    request.session.flush()  # Clear all session data
    messages.success(request, 'You logged out')
    return redirect('app1:index')




