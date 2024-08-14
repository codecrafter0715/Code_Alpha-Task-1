import logging
from venv import logger
from django.conf import settings
from django.db.models import Count
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views import View
import stripe
from . models import Cart, Customer, OrderPlaced, Product, Payment
from . forms import CustomerProfileForm, CustomerRegistrationForm, MySetPasswordForm
from django.contrib import messages
from django.contrib.auth.views import PasswordResetConfirmView
from django.db.models import Q

# Create your views here.
def home(request):
    return render(request,"app/home.html")

def about(request):
    return render(request, "app/about.html")

def contact(request):
    return render(request, "app/contact.html")

class CategoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())

class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())
    
class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        return render(request,"app/productdetail.html",locals())
    
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Register Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/customerregistration.html',locals())

class ProfileView(View):
    def get(self, request):
        user = request.user
        # Check if user is authenticated
        if user.is_authenticated:
            customer = Customer.objects.filter(user=user).first()
            form = CustomerProfileForm(instance=customer)
            return render(request, 'app/profile.html', {'form': form})
        else:
            return redirect('login')  # Redirect to login if user is not authenticated

    def post(self, request):
        user = request.user
        # Check if user is authenticated
        if user.is_authenticated:
            customer = Customer.objects.filter(user=user).first()
            form = CustomerProfileForm(request.POST, instance=customer)

            if form.is_valid():
                form.save()
                messages.success(request, "Congratulations! Profile Saved Successfully")
                return redirect('profile')  # Redirect to profile after saving
            else:
                messages.warning(request, "Invalid Input Data")
            
            return render(request, 'app/profile.html', {'form': form})
        else:
            return redirect('login')  # Redirect to login if user is not authenticated

def process_payment(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        payment_method = request.POST.get('payment_method')
        transaction_id = request.POST.get('transaction_id')
        try:
            order = OrderPlaced.objects.get(id=order_id)
            payment = Payment(
                order_id=order_id,
                payment_method=payment_method,
                transaction_id=transaction_id,
                payment_status='Pending',  # You may update this based on payment processing
                paid=False,
                payment_date=None
            )
            payment.save()
            messages.success(request, 'Payment recorded. Awaiting confirmation.')
            return redirect('order_summary', order_id=order_id)
        except OrderPlaced.DoesNotExist:
            messages.error(request, 'Order not found.')
            return redirect('checkout')
    else:
        return redirect('checkout')

def checkout(request):
    order = get_object_or_404(OrderPlaced, user=request.user, status='Pending')
    cart_items = order.items.all()  # Adjust according to your cart logic
    total_amount = sum(item.product.discounted_price * item.quantity for item in cart_items)
    addresses = request.user.address_set.all()  # Adjust according to your address model
    
    return render(request, 'app/checkout.html', {
        'order': order,
        'cart_item': cart_items,
        'totalamount': total_amount,
        'add': addresses,
    })

def view_cart(request):
    """View to display the cart."""
    cart = get_or_create_cart(request.user)
    cart_items = cart.items.all()
    context = {'cart_items': cart_items}
    return render(request, 'cart/view_cart.html', context)

def get_or_create_cart(user):
    """Get or create a cart for the user."""
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


def payment_page(request):
    # Example context, adjust as needed
    return render(request, 'app/payment.html')

logger = logging.getLogger(__name__)
def process_payment(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id', '')
        payment_method = request.POST.get('payment_method', '')
        transaction_id = request.POST.get('transaction_id', '')
        
        logger.debug(f'Received order_id: "{1}"')
        logger.debug(f'Received payment_method: "{payment_method}"')
        logger.debug(f'Received transaction_id: "{transaction_id}"')

        if not order_id:
            return HttpResponseBadRequest("Order ID is required.")

        # Process payment
        # ...

        return redirect('success_page')
    else:
        return HttpResponseBadRequest("Invalid request method.")

def process_payment(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id', '')
        payment_method = request.POST.get('payment_method', '')
        transaction_id = request.POST.get('transaction_id', '')
        
        if not order_id:
            return HttpResponseBadRequest("Order ID is required.")
        
        # Process the payment
        # ...

        return redirect('success_page')
    else:
        return HttpResponseBadRequest("Invalid request method.")

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',locals())

@login_required
def update_address(request, pk):
    customer = get_object_or_404(Customer, pk=pk, user=request.user)

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Address updated successfully.")
            return redirect('address')  # Adjust redirect as needed
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomerProfileForm(instance=customer)

    return render(request, 'app/updateAddress.html', {'form': form})

def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount += value  # Correctly accumulate the total value
    
    totalamount = amount * 1.40  # Adding 40% tax to the amount

    amount = round(amount, 2)
    totalamount = round(totalamount, 2)

    # Prepare the context to be passed to the template
    context = {
        'cart': cart,
        'amount': amount,
        'totalamount': totalamount
    }
    
    # Render the template with the context
    return render(request, 'app/addtocart.html', context)


class checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        return render(request, 'app/checkout.html',locals())

def checkout_view(request):
    # Your view logic here
    return render(request, 'app/checkout.html')

def orders(request):
    """View to display user orders."""
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',locals())

#def orders(request):
#    order_placed=OrderPlaced.objects,filter(user=request.user)
#    return render(request, 'app/orders.html',locals()),

def plus_cart(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(uuser=request.user))
        c.quantity=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        #print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(uuser=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        #print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(uuser=request.user))
        c.quantity-=1
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        #print(prod_id)
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)



