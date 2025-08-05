from django.shortcuts import render, get_object_or_404
from .models import Product

# def home(request):
#     products = Product.objects.all()
#     return render(request, 'shop/home.html', {'products': products})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

def home(request):
    sort = request.GET.get('sort')
    category = request.GET.get('category')

    products = Product.objects.all()
    if category:
        products = products.filter(category__iexact=category)
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')

    return render(request, 'shop/home.html', {'products': products})

from django.shortcuts import redirect, get_object_or_404
from .models import Product

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity

    request.session['cart'] = cart
    return redirect('cart')  # Or redirect back to the same product detail page

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, qty in cart.items():
        product = Product.objects.get(pk=product_id)
        subtotal = product.price * qty
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': qty,
            'subtotal': subtotal
        })

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('cart')



# views.py
import google.generativeai as genai
from django.shortcuts import render
from .models import Product  # assuming you have a Product model

# Load API key
genai.configure(api_key='AIzaSyCyuWDy2yWInRyjbFTyop6bA9UxZ7Tc7GI')

def ai_recommendation(request):
    products = Product.objects.all()
    product_names = ', '.join([p.name for p in products]) if products else "No products available"
    
    prompt = f"Recommend top 3 products from the following: {product_names}"

    try:
        model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
        response = model.generate_content(prompt)
        recommendations = response.text
    except Exception as e:
        recommendations = f"AI Error: {str(e)}"

    return render(request, 'shop/recommend.html', {
        'recommendations': recommendations,
        'products': products
    })

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review  # assuming you have Review model

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST' and 'review_submit' in request.POST:
        name = request.POST.get('name')
        comment = request.POST.get('comment')
        if name and comment:
            Review.objects.create(product=product, reviewer_name=name, comment=comment)
            return redirect('product_detail', product_id=product.id)
    
    reviews = product.reviews.all().order_by('-created_at')

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'reviews': reviews,
        # include other context like cart_item_count if needed
    })

