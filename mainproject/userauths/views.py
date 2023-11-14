from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from app1.backends import EmailBackend  # Import your custom authentication backend

from userauths.models import User  # Import your custom user model


# def index(request):
#     return render(request, 'app1/index.html')

def register_view(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.sucess(request, f'Hey {username}, Your account was created succesfully')
            # login(request, user)
            return redirect('login')  # Redirect to the desired page after successful registration
    else:
        form = CreateUserForm()

    context = {'form': form}
    return render(request, 'userauths/signup.html', context)

def login_view(request):
  
    if request.user.is_authenticated:
      messages.warning(request,f"Hey You are already logged in")
      return redirect("index")
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)
        try:
          user = User.objects.get(email=email)
          user = authenticate(email=email, password=password,backend = EmailBackend)
        

          if user is not None:
              login(request, user)
              request.session['logged_in'] = True  # Set a session variable if needed
              messages.success(request, 'Login successful.')
              return redirect("index")  # Redirect to the desired page after successful login
          else:
              messages.warning(request, 'Username or Password is incorrect.')

        except:
          messages.warning(request, f'User with {email} doesnot exists')
          
        
    context = {}
    return render(request, 'userauths/login.html', context)


def logoutUser(request):
    logout(request)
    messages.success(request,f'You logged out')
    return redirect('userauths:login') 




