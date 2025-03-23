from django.shortcuts import render,redirect
from .models import *

# Create your views here.
def index(request):
    return render(request,'index.html')

def shop(request):
    return render(request,'shop.html')

def shop_cart(request):
    return render(request,'shop-cart.html')

def product_details(request):
    return render(request,'product-details.html')

def contact(request):
    return render(request,'contact.html')

def checkout(request):
    return render(request,'checkout.html')

def login(request):
    # Attempt to retrieve the user based on the email stored in the session
    try:
        user = User.get(email=request.session['email'])

        return render(request,'index.html',{'user':user})
    except:

        if request.method == 'POST':
            try:
                user = User.objects.get(email=request.POST['email'])

                if request.POST['password'] == user.password:
                    request.session['email'] = user.email
                    return render(request,'index.html',{'user':user})
                return render(request, 'login.html', {'msg': 'Incorrect Password'})

                
            except:
                return render(request, 'signup.html', {'msg': 'Account does not exist, please sign up'})


        return render(request,'login.html')

def signup(request): 
    # Handle user registration

    if request.method =='POST':
        if request.POST['password'] == request.POST['cpassword']:
            try:
                User.objects.get(email=request.POST['email'])
                return render(request, 'login.html', {'msg': 'Account already exists, please sign in'})

            except:
                User.objects.create(
                    name=request.POST['name'],
                    email=request.POST['email'],
                    mobile=request.POST['mobile'],
                    password=request.POST['password']        
            )
            return render(request, 'login.html', {'msg': 'Account created, go and login'})

        
        return render(request, 'signup.html', {'msg': 'Both passwords are not the same'})

    
    return render(request,'signup.html')
