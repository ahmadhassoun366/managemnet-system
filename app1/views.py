from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Space
from .forms import SpaceForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)

navigation = [
    {'label': 'Home', 'href': '/'},
    {'label': 'Products', 'href': '/products'},
    {'label': 'About', 'href': '/about'},
]

socials = [
    {'label': 'Facebook', 'href': 'https://facebook.com', 'icon': 'fab fa-facebook-f'},
    {'label': 'Twitter', 'href': 'https://twitter.com', 'icon': 'fab fa-twitter'},
    {'label': 'Instagram', 'href': 'https://instagram.com', 'icon': 'fab fa-instagram'},
]
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('list_spaces')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password', 'navigation': navigation, 'socials': socials})
    else:
        return render(request, 'login.html', {'navigation': navigation, 'socials': socials})
    
def logout(request):
    auth_logout(request)
    return redirect('/')

@login_required
def list_spaces(request):
    spaces = Space.objects.filter(user=request.user)
    return render(request, 'list_spaces.html', {'spaces': spaces, 'navigation': navigation, 'socials': socials})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('list_spaces')
        else:
            logger.error("Form is not valid: %s", form.errors)
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form, 'navigation': navigation, 'socials': socials})

@login_required
def list_spaces(request):
    spaces = Space.objects.filter(user=request.user)
    return render(request, 'list_spaces.html', {'spaces': spaces,'navigation': navigation, 'socials': socials})

def create_update_space(request, space_id=None):
    if space_id:
        space = Space.objects.get(id=space_id)
        if request.method == 'POST':
            form = SpaceForm(request.POST, instance=space)
            if form.is_valid():
                form.save()
                return redirect(reverse('list_spaces'))
        else:
            form = SpaceForm(instance=space)
    else:
        if request.method == 'POST':
            form = SpaceForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(reverse('list_spaces'))
        else:
            form = SpaceForm()

    return render(request, 'space_form.html', {'form': form,'navigation': navigation, 'socials': socials})

def delete_space(request, space_id):
    space = Space.objects.get(id=space_id)
    space.delete()
    messages.success(request, "Space deleted successfully!")
    return redirect(reverse('list_spaces'))

def make_reservation(request, space_id):
    space = Space.objects.get(id=space_id)
    if request.method == 'POST':
        # Assuming you have a ReservationForm to handle this
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.space = space
            reservation.save()
            return redirect(reverse('list_spaces'))
    else:
        form = ReservationForm()

    return render(request, 'make_reservation.html', {'form': form, 'space': space,'navigation': navigation, 'socials': socials})

def request_service(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    if request.method == 'POST':
        # Process service request
        pass
    return render(request, 'request_service.html', {'reservation': reservation,'navigation': navigation, 'socials': socials})
