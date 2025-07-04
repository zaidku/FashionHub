from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.core.paginator import Paginator
from app.models import Sale, SaleItem, Customer, Product, ProductImage
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib import messages
from app.models import Product
import uuid




# Create your views here.
from django.shortcuts import render, get_object_or_404
from app.models import Product  # reusing your admin Product model

def home(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'storefront/home.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'storefront/product_detail.html', {'product': product})

def product_list(request):
    products = Product.objects.filter(is_active=True).order_by('-id')
    
    # Optional: Add pagination
    paginator = Paginator(products, 12)  # 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'storefront/product_list.html', {
        'products': page_obj
    })


#--------------------------------------------#
# Store Front operations, ordering and extra #
#--------------------------------------------#


# Order item action
@csrf_exempt
def place_order(request, slug):
    if request.method == 'POST':
        product = get_object_or_404(Product, slug=slug)
        quantity = int(request.POST.get('quantity', 1))

        if product.quantity < quantity:
            return render(request, 'storefront/product_detail.html', {
                'product': product,
                'error': 'Not enough stock available'
            })

        # 🧾 Get customer info
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city')
        state = request.POST.get('state')
        payment_method = request.POST.get('payment_method')  # 'CARD', 'ZELLE', etc.

        full_address = f"{address1} {address2}, {city}, {state}"

        # 👤 Create or find the customer
        customer, _ = Customer.objects.get_or_create(
            email=email,
            defaults={
                'name': name,
                'phone': phone,
                'address': full_address
            }
        )

        # 💵 Calculate totals
        subtotal = product.price * quantity
        tax = subtotal * 0.08  # Optional: 8% tax example
        total = subtotal + tax

        # 🧾 Create the sale
        sale = Sale.objects.create(
            invoice_number=uuid.uuid4().hex[:8].upper(),
            customer=customer,
            payment_method=payment_method,
            subtotal=subtotal,
            tax=tax,
            total=total
        )

        # 🛒 Sale item
        SaleItem.objects.create(
            sale=sale,
            product=product,
            quantity=quantity,
            unit_price=product.price,
            total_price=subtotal
        )

        # 🏷️ Update product stock
        product.quantity -= quantity
        product.save()

        # ✅ Show confirmation page
        return render(request, 'storefront/thank_you.html', {
            'product': product,
            'sale': sale
        })

    return redirect('storefront:product_list')



#-------------------------------------------#
#              Shopping Cart Area           #
#-------------------------------------------#

# shopping car view 
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for slug, quantity in cart.items():
        try:
            product = get_object_or_404(Product, slug=slug)
            subtotal = product.price * quantity
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
        except Product.DoesNotExist:
            # Remove invalid products from cart
            del cart[slug]
            request.session.modified = True
    
    return render(request, 'storefront/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

def add_to_cart(request, slug):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        quantity = int(request.POST.get('quantity', 1))
        
        if slug in cart:
            cart[slug] += quantity
        else:
            cart[slug] = quantity
            
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, "Item added to your cart")
        return redirect('storefront:product_list')
    
    return redirect('storefront:product_list')

def remove_from_cart(request, slug):
    cart = request.session.get('cart', {})
    
    if slug in cart:
        del cart[slug]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, "Item removed from your cart")
    
    return redirect('storefront:cart')

def update_cart(request, slug):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart[slug] = quantity
        else:
            del cart[slug]
            
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, "Cart updated")
    
    return redirect('storefront:cart')

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty")
        return redirect('storefront:cart')
    
    # Process payment and create order here
    # ...
    
    # Clear cart after successful checkout
    request.session['cart'] = {}
    request.session.modified = True
    
    return render(request, 'storefront/thank_you.html')