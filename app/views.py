from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, HttpResponsePermanentRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(requests):
    data=Products.objects.all().order_by('-create_date')
    return render(requests,  'home.html', {'data':data})

def sign__up(requests):
     if requests.method == 'POST' :
        uname=requests.POST.get('username')
        email=requests.POST.get('email')        
        pass1=requests.POST.get('password1')
        pass2=requests.POST.get('password2')
        
        
        if pass1 != pass2:
            return HttpResponse("Password are not same")
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            
            profile = Profile(
                var=my_user,
                user_address_1='none',  # Provide the user's address
                user_address_2='none',  # Provide the user's address
                user_pincode='none',    # Provide the user's pincode
                user_email=email,   # Use the same email as the user
                user_phone='none'       # Provide the user's phone number
            )
            profile.save()
        
                         
            return redirect('home')
        
     return render (requests, 'signup.html')
    
def log__in(requests):
    if requests.method == 'POST':
     uname=requests.POST.get('username')
     pass1=requests.POST.get('password')
     user=authenticate(requests,username=uname, password=pass1)
            
     if user is not None:
            login(requests,user)
            return redirect('home')
     else:
         return HttpResponse("Username and Password is incorrect")
    return render(requests, 'login.html')

def log__out(requests):
    logout(requests)
    messages.success(requests, ("You were Logged out"))
    return redirect('home')

def product_detail(requests,pk):
    data=Products.objects.get(id=pk)
    return render(requests, 'product_detail.html', {'data':data })

@login_required
def my_account(requests):
    return render(requests ,'my_account.html')


def search_product(request):
    zata = Products.objects.all()
    search_query = request.GET.get('q')  # Retrieve the search query from the GET request
    search_query2 = request.GET.get('name')  # Retrieve the search query from the GET request
    
    if search_query:
         zata = zata.filter(product_name__icontains=search_query) | zata.filter(product_details__icontains=search_query)
    context = {
        'zata': zata,
    }

    if search_query2:
            zata = zata.filter(product_name__icontains=search_query2) | zata.filter(product_details__icontains=search_query2)
    context = {
        'zata': zata,
    }    
    return render(request, 'home.html', context)

from django.contrib import messages
from decimal import Decimal, InvalidOperation
from django.db.models import Sum, ExpressionWrapper, DecimalField, F, FloatField
from decimal import Decimal


def calculate_total(cart):
    if cart is None:
        return Decimal('0.00')
    
    total_price = cart.cartitem_set.annotate(
        item_total=ExpressionWrapper(
            F('product__product_price') * F('quantity'),
            output_field=DecimalField()
        )
    ).aggregate(total=Sum('item_total'))

    return total_price['total'] or Decimal('0.00')


@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Products, pk=id)
    user_profile = get_object_or_404(Profile, var=request.user)

  
    user_input = request.POST.get('quantity')

    try:
        decimal_quantity = Decimal(user_input)
    except InvalidOperation:
        messages.error(request, "Invalid quantity. Please enter a valid number.")
        return redirect('view_cart')

    if decimal_quantity <= 0:
        messages.error(request, "Quantity must be greater than zero.")
        return redirect('view_cart')

 
    cart, created = Cart.objects.get_or_create(user=user_profile)

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if item_created:
        cart_item.quantity = decimal_quantity
    else:
        cart_item.quantity = decimal_quantity
        

    cart_item.save()
    messages.success(request, f"{product.product_name} quantity has been updated.")

   
    print("Cart item added successfully")
    print(f"Cart ID: {cart.id}, Product ID: {product.id}, Quantity: {cart_item.quantity}")

    return redirect('view_cart')


@login_required
def remove_from_cart(request, id):
    # Retrieve the cart item
    cart_item = get_object_or_404(CartItem, id=id)

    # Check if the user has permission to delete the cart item
    if cart_item.cart.user != request.user:
        # Handle unauthorized deletion (e.g., return an error response)
        pass

    cart_item.delete()
    messages.success(request, "Cart item deleted successfully.")

    return redirect('view_cart')


@login_required
def view_cart(request):
    try:
        user_profile = Profile.objects.get(var=request.user)
        cart, created = Cart.objects.get_or_create(user=user_profile)
        cart_items = CartItem.objects.filter(cart=cart)
    except Profile.DoesNotExist:
        print("error h bai ")

    if request.method == "POST":
        for cart_item in cart_items:
            new_quantity_str = request.POST.get(f"quantity-{cart_item.id}")
            
            if new_quantity_str == None:
                print("ERROR H BAI")
            else:
                new_quantity = Decimal(new_quantity_str)
                print(new_quantity)
                cart_item.quantity = new_quantity
                cart_item.save()
                
    total_amount = calculate_total(cart) if cart else Decimal('0.00')
    quantity_range = range(1, 11)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_amount': total_amount})


@login_required
def checkout(request):
    # Get the user's cart
    user_profile = Profile.objects.get(var=request.user)
    cart = Cart.objects.get(user=user_profile)

    total_amount = calculate_total(cart)
    
    if request.method == "POST":
   
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount
        )

        for cart_item in cart.cartitem_set.all():
            order.items.add(cart_item.product)
        cart.cartitem_set.all().delete()
        
        
        return redirect('order_confirmation')


@login_required
def order_confirmation(request):

    order = Order.objects.filter(user=request.user).latest('order_date')

    return render(request, 'confirmation.html', {'order': order})


#################################  MAil Sending and Download PDF Functionality ##########################3

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas

@receiver(post_save, sender=Order)
def create_bill(sender, instance, created, **kwargs):
    if created:
        total_amount = instance.total_amount
        bill = Bill.objects.create(order=instance, total_amount=total_amount)
        print(f"Created Bill with ID: {bill.id}")
        
        subject = "Your Order Bill"
        message = "Please find your order bill attached."
        from_email = settings.EMAIL_HOST_USER  # Replace with your email address
        recipient_list = [instance.user.email]  # User's email address
        
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        user = bill.order.user
        p.drawString(100, 780, "Amazon service")
        p.drawString(100, 760, "GST: ABCD1234")
        p.drawString(100, 740, f'Bill Order ID: {bill.order.id}')
        p.drawString(100, 720, f'Customer Name: {user.username}')
        p.drawString(100, 700, f'Customer Email: {user.email}')
        p.drawString(100, 680, f'Total Amount: Rs. {bill.total_amount}')
        p.showPage()
        p.save()
        
        buffer.seek(0)

        pdf_filename = f'bill_{bill.id}.pdf'
        msg = EmailMessage(subject, message, from_email, recipient_list)
        msg.attach(pdf_filename, buffer.read(), 'application/pdf')
        msg.send()

@login_required
def generate_pdf_bill(requests, id):
    print(f"Requested Bill ID: {id}")
    bill = Bill.objects.get(id=id)  
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bill_{bill.id}.pdf"'
    user = bill.order.user
    p = canvas.Canvas(response)
    
    p.drawString(100, 780, "Amazon service")
    p.drawString(100, 760, "GST: ABCD1234")
    p.drawString(100, 740, f'Bill Order ID: {bill.order.id}')
    p.drawString(100, 720, f'Customer Name: {user.username}')
    p.drawString(100, 700, f'Customer Email: {user.email}')
    y = 680
    for product in bill.order.items.all():
        try:
            # cart_item = CartItem.objects.get(cart__user=bill.order.user, product=product)
            p.drawString(120, y, f'Product Name: {product.product_name}')
            # p.drawString(320, y, f'Quantity: {cart_item.quantity}')
            y -= 20
        except CartItem.DoesNotExist:
            pass  # Handle the case where the CartItem is not found for the product
    
    p.drawString(400, 550, f'Total Amount: Rs. {bill.total_amount}')
    p.showPage()
    p.save()    

    return response


@login_required
def my_order(requests):
    orders = Order.objects.filter(user=requests.user).order_by('-order_date')
    # data=Bill.objects.filter(order=requests.user)
    return render(requests, 'my_order.html',{'orders': orders})


@receiver(post_save, sender=Profile)
def create_cart_for_profile(sender, instance, created, **kwargs):
    if created:
        # Create a new Cart associated with the Profile
        Cart.objects.create(user=instance)









    
    