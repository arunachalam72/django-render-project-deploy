from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Case, When, IntegerField
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
import stripe
import json
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import *
from django.contrib.auth import authenticate,login,logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError, AccessToken

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def register_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            username = data.get("username")
            email = data.get("email")
            password1 = data.get("password1")
            password2 = data.get("password2")

            # validation
            if not username or not email or not password1:
                return JsonResponse({"status": "error", "message": "All fields required"}, status=400)

            if password1 != password2:
                return JsonResponse({"status": "error", "message": "Passwords do not match"}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"status": "error", "message": "Username exists"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"status": "error", "message": "Email exists"}, status=400)

            # IMPORTANT FIX: create_user (correct hashing)
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )

            return JsonResponse({
                "status": "success",
                "message": "User created successfully"
            })

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"message": "Invalid method"}, status=405)

def logout_api(request):
    response = JsonResponse({"status": "logged out"})

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home_api(request):
    return response({"message": "Authenticated"})


# =========================================
# 🔹 LOGIN API (JWT AUTH)
# =========================================

@csrf_exempt
def login_api(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return JsonResponse({
                "status": "error",
                "message": "Invalid credentials"
            }, status=401)

        # 🔥 IMPORTANT: this sets request.user
        login(request, user)

        refresh = RefreshToken.for_user(user)

        response = JsonResponse({
            "status": "success"
        })

        response.set_cookie("access_token", str(refresh.access_token), httponly=True)
        response.set_cookie("refresh_token", str(refresh), httponly=True)

        return response

@csrf_exempt
def refresh_token_api(request):
    try:
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return JsonResponse({"error": "No refresh token"}, status=401)

        refresh = RefreshToken(refresh_token)
        new_access = str(refresh.access_token)

        response = JsonResponse({"status": "refreshed"})
        response.set_cookie("access_token", new_access, httponly=True)

        return response

    except TokenError:
        return JsonResponse({"error": "Invalid token"}, status=401)

def Register_page(request):
    return render(request, 'EcommerceApp/Register.html')


def Login_page(request):
    return render(request, 'EcommerceApp/Login.html')

def search_suggestions(request):
    query = request.GET.get('q', '')
    data = []

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(description__icontains=query)
        ).annotate(
            priority=Case(
                When(name__istartswith=query, then=0),   # 🔥 highest priority
                When(name__icontains=query, then=1),
                default=2,
                output_field=IntegerField()
            )
        ).filter(status=False).order_by('priority')[:8]

        for p in products:
            data.append({
                'id': p.id,
                'name': p.name,
                'price': p.selling_price,
                'image': p.product_image.url if p.product_image else ''
            })

    return JsonResponse(data, safe=False)

def Service_page(request):
    return render(request,'EcommerceApp/Service.html')

def Logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')

def Home_page(request):
    categories = Catagory.objects.filter(status=False)[:6]
    trending_products = Product.objects.filter(trending=True, status=False)[:8]
    favorite_ids = []
    if request.user.is_authenticated:
        favorite_ids = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
    context = {
        'categories': categories,
        'trending_products': trending_products,
        'favorite_ids': favorite_ids
    }
    return render(request, 'EcommerceApp/Home.html', context)

@login_required
def Profile_update(request, id):
    user_obj = get_object_or_404(User, id=id)

    if request.user != user_obj:
        return redirect('home')

    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=user_obj)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UpdateProfileForm(instance=user_obj)

    return render(request, 'EcommerceApp/Profile_edit.html', {'form': form})


def About_page(request):
    return render(request,'EcommerceApp/About.html')

def Catagory_page(request):
    #if request.user.is_authenticated:
    products = Catagory.objects.all()
    return render(request,'EcommerceApp/Catagory.html',{'products':products})
    #return redirect('home')


def Contact_page(request):
    return render(request,'EcommerceApp/Contact.html')

def Product_page(request, name):

    token = request.COOKIES.get("access_token")

    if not token:
        return redirect("login")

    category_name = name.replace("-", " ")

    products = Product.objects.filter(
        category__name__iexact=category_name
    )

    max_price = request.GET.get('max_price')

    if max_price and max_price.isdigit():
        products = products.filter(
            selling_price__lte=int(max_price)
        )

    favorite_ids = []

    if request.user.is_authenticated:
        favorite_ids = Favorite.objects.filter(
            user=request.user
        ).values_list('product_id', flat=True)

    return render(
        request,
        'EcommerceApp/Product.html',
        {
            'products': products,
            'selected_price': max_price or 200000,
            'favorite_ids': list(favorite_ids),
        }
    )

def product_detail(request, id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=id)

        # Fetch related products from the same category (excluding the current product)
        related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

        return render(request, 'EcommerceApp/Product_details.html', {
            'product': product,
            'related_products': related_products
        })
    return redirect('home')

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.quantity * item.product.selling_price for item in cart_items)
    return render(request, 'EcommerceApp/Cart.html', {'cart_items': cart_items, 'total': total})


def update_cart_quantity(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        product = cart_item.product

        try:
            new_quantity = int(request.POST.get('quantity', 1))
            if new_quantity < 1:
                new_quantity = 1
        except (ValueError, TypeError):
            new_quantity = cart_item.quantity

        # Adjust product stock
        diff = new_quantity - cart_item.quantity
        if product.quantity < diff:
            # Not enough stock
            new_quantity = cart_item.quantity + product.quantity
            diff = new_quantity - cart_item.quantity

        product.quantity -= diff
        product.save()

        cart_item.quantity = new_quantity
        cart_item.save()

    return HttpResponseRedirect(reverse('cart'))


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        quantity = int(request.GET.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except (ValueError, TypeError):
        quantity = 1

    if product.quantity < quantity:
        return JsonResponse({'success': False, 'message': 'Not enough stock!'})

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        # Add quantity if already in cart
        cart_item.quantity += quantity
        cart_item.save()
    
    # Decrease product stock
    product.quantity -= quantity
    product.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'quantity': cart_item.quantity,
            'total_price': cart_item.quantity * product.selling_price
        })

    return redirect('cart')


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')


def update_cart(request, cart_item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
        product = cart_item.product
        new_quantity = int(request.POST.get("quantity", 1))
        old_quantity = cart_item.quantity
        quantity_change = new_quantity - old_quantity  # positive if increased, negative if decreased

        # Check if increasing quantity exceeds available stock
        if quantity_change > 0:
            if product.quantity >= quantity_change:
                product.quantity -= quantity_change
                product.save()
                cart_item.quantity = new_quantity
                cart_item.save()
                messages.success(request, "Cart updated successfully.")
            else:
                messages.error(request, f"Only {product.quantity} items left in stock.")
        else:  # Decreasing quantity, return stock to product
            product.quantity -= quantity_change  # subtracting negative = add back
            product.save()
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, "Cart updated successfully.")

        return redirect('cart')

    return redirect('cart')

@login_required
def favorite_list(request):
    """Display all favorite products of the logged-in user."""
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    return render(request, 'EcommerceApp/Favourite.html', {'favorites': favorites})

@login_required
def toggle_favorite(request, product_id):
    # Get the product object or return 404
    product = get_object_or_404(Product, id=product_id)

    # Try to get or create a Favorite object
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)

    if not created:
        # Already exists, remove from favorites
        favorite.delete()
        is_favorite = False
    else:
        # Added to favorites
        is_favorite = True

    # Return JSON response for AJAX
    return JsonResponse({'is_favorite': is_favorite})

def product_list(request):
    selected_price = request.GET.get('max_price', 200000)
    products = Product.objects.filter(selling_price__lte=selected_price)

    favorite_ids = []
    if request.user.is_authenticated:
        favorite_ids = list(Favorite.objects.filter(user=request.user).values_list('product_id', flat=True))

    return render(request, 'EcommerceApp/Product.html', {
        'products': products,
        'selected_price': selected_price,
        'favorite_ids': favorite_ids,
    })


@login_required
def add_to_favorite(request, product_id):
    """Add a product to user's favorites."""
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    
    if created:
        messages.success(request, f"{product.name} has been added to your favorites!")
    else:
        messages.info(request, f"{product.name} is already in your favorites.")
    
    return redirect('favorites')  # Redirect to favorites page


@login_required
def remove_from_favorite(request, product_id):
    """Remove a product from favorites."""
    favorite = Favorite.objects.filter(user=request.user, product_id=product_id)
    if favorite.exists():
        favorite.delete()
        messages.success(request, "Item removed from your favorites.")
    else:
        messages.warning(request, "This product is not in your favorites.")
    
    return redirect('favorites')

# @login_required
# def checkout(request):
#     cart_items = CartItem.objects.filter(user=request.user)

#     if not cart_items:
#         return redirect('home')

#     total = sum(item.total_price for item in cart_items)

#     # Create order (Pending)
#     order = Order.objects.create(
#         user=request.user,
#         total_amount=total
#     )

#     for item in cart_items:
#         OrderItem.objects.create(
#             order=order,
#             product=item.product,
#             quantity=item.quantity,
#             price=item.product.selling_price
#         )

#     return render(request, 'EcommerceApp/Checkout.html', {
#         'order': order,
#         'stripe_public_key': settings.STRIPE_PUBLIC_KEY
#     })

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import CartItem, Order, OrderItem

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    # FIX: proper empty check
    if not cart_items.exists():
        return redirect('home')

    # FIX: correct total calculation
    total = sum(item.product.selling_price * item.quantity for item in cart_items)

    # Create order
    order = Order.objects.create(
        user=request.user,
        total_amount=total
    )

    # Create order items
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.selling_price
        )

    return render(request, 'EcommerceApp/Checkout.html', {
        'order': order,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })

# @require_POST
def create_stripe_session(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)

    line_items = []

    for item in order.items.all():
        line_items.append({
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': item.product.name,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('payment_success', args=[order.order_id])
        ),
        cancel_url=request.build_absolute_uri(
            reverse('payment_cancel', args=[order.order_id])
        ),
    )

    return JsonResponse({'id': session.id})

def payment_success(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)

    order.status = "Paid"
    order.save()

    # Clear cart
    CartItem.objects.filter(user=request.user).delete()

    return render(request, 'EcommerceApp/Payment_success.html', {'order': order})

def payment_cancel(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    order.status = "Cancelled"
    order.save()

    return render(request, 'EcommerceApp/Payment_cancel.html', {'order': order})


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'EcommerceApp/Order_list.html'
    context_object_name = 'orders'
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        # Superuser sees all orders, regular users see only their own
        if user.is_superuser:
            return Order.objects.all().order_by('-created_at')
        return Order.objects.filter(user=user).order_by('-created_at')