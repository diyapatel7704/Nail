from django.shortcuts import render,redirect,get_object_or_404
from .models import *

# Create your views here.
def index(request):
    if 'email' not in request.session:
        return redirect('login') 
    categories = Category.objects.all()  # Fetch all categories
    products = Product.objects.all()  # Fetch all products
    return render(request, "index.html", {"categories": categories, "products": products})

  

def shop(request):
    category_id = request.GET.get("category")  # Get category filter from URL
    
    if category_id:
        try:
            category_id = int(category_id)  # Ensure category_id is an integer
            products = Product.objects.filter(category_id=category_id)  # Filter by category
        except ValueError:
            products = Product.objects.all()  # If conversion fails, return all products
    else:
        products = Product.objects.all()  # Get all products

    categories = Category.objects.all()  # Fetch all categories
    return render(request, "shop.html", {"categories": categories, "products": products})


def shop_cart(request):
    return render(request,'shop-cart.html')


def product_detail(request, id):

    product = get_object_or_404(Product, id=id)
    related_products = Product.objects.filter(category_id=product.category_id).exclude(id=product.id)[:4]

    return render(request, "product-details.html", {
        "product": product,
        "related_products": related_products,
    })


def contact(request):
    return render(request,'contact.html')

def shop_cart(request):
    """Displays all cart items for the logged-in user."""
    if 'email' not in request.session:
        return redirect('login')  # Redirect if user is not logged in

    user = get_object_or_404(User, email=request.session['email'])
    cart_items = Cart.objects.filter(user=user)

    cart_total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'shop-cart.html', {'cart_items': cart_items, 'cart_total': cart_total})

def add_to_cart(request, product_id):
    """Adds a product to the cart or updates the quantity if it already exists."""
    if 'email' not in request.session:
        return redirect('login')

    user = get_object_or_404(User, email=request.session['email'])
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(user=user, product=product)

    if not created:
        cart_item.quantity += 1  # Increase quantity if product exists in cart
    cart_item.save()

    return redirect('shop_cart')

def remove_from_cart(request, cart_id):
    """Removes an item from the cart."""
    if 'email' not in request.session:
        return redirect('login')

    user = get_object_or_404(User, email=request.session['email'])
    cart_item = get_object_or_404(Cart, id=cart_id, user=user)

    cart_item.delete()
    return redirect('shop_cart')

def checkout(request):
    """Redirects to the checkout page with the total amount."""
    if 'email' not in request.session:
        return redirect('login')

    user = get_object_or_404(User, email=request.session['email'])
    cart_items = Cart.objects.filter(user=user)
    cart_total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'checkout.html', {'cart_total': cart_total})

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

def logout(request):
    del request.session['email']
    return redirect('login/')

