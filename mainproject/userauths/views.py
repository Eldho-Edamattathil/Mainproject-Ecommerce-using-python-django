from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from app1.backends import EmailBackend  # Import your custom authentication backend
import random
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password

from userauths.models import User  # Import your custom user model


# def index(request):
#     return render(request, 'app1/index.html')

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
            
            # login(request, user)
            # return redirect('userauths:login')  # Redirect to the desired page after successful registration
    else:
        form = CreateUserForm()

    context = {'form': form}
    return render(request, 'userauths/signup.html', context)


#OTP
def send_otp(request):
    s=""
    for x in range(0,4):
        s+=str(random.randint(0,9))
    request.session["otp"]=s
    send_mail("otp for sign up",s,'djangoalerts0011@gmail.com',[request.session['email']],fail_silently=False)
    return render(request,"userauths/otp.html")


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
            #   request.session['logged_in'] = True  # Set a session variable if needed
              messages.success(request, 'Login successful.')
              return redirect("app1:index")  # Redirect to the desired page after successful login
          else:
              messages.warning(request, 'Username or Password is incorrect.')

        except:
          messages.warning(request, f'User with {email} doesnot exists')
          
        
    context = {}
    return render(request, 'userauths/login.html', context)


def logoutUser(request):
    logout(request)
    messages.success(request,f'You logged out')
    return redirect('app1:index') 




