import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Service, Booking, BookingItem, Review
from .forms import UserRegistrationForm, BookingForm, ReviewForm

def home(request):
    services = Service.objects.all()
    
    # Filter Logic
    category = request.GET.get('category')
    search = request.GET.get('search')
    if category:
        services = services.filter(category=category)
    if search:
        services = services.filter(name__icontains=search)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        
        cart_data = request.POST.get('cart_json')
        form = BookingForm(request.POST)
        
        if form.is_valid() and cart_data:
            try:
                cart_items = json.loads(cart_data)
                if not cart_items:
                    messages.error(request, "Your cart is empty!")
                    return redirect('home')

                booking = form.save(commit=False)
                booking.user = request.user
                booking.save() # Get ID
                
                total = 0
                for item in cart_items:
                    service = Service.objects.get(id=item['id'])
                    qty = int(item['quantity'])
                    BookingItem.objects.create(booking=booking, service=service, quantity=qty, price=service.price)
                    total += (service.price * qty)
                
                booking.total_amount = total
                booking.save()
                messages.success(request, "Booking Successful!")
                return redirect('my_bookings')
            except Exception as e:
                print(e)
                messages.error(request, "Something went wrong.")
    
    else:
        form = BookingForm()

    return render(request, 'home.html', {'services': services, 'form': form})

@login_required
def my_bookings_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-date_created')
    return render(request, 'my_bookings.html', {'bookings': bookings})

@login_required
def add_review(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.service = service
            review.save()
            return redirect('home')
    return redirect('home')

def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')