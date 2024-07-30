from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Space, Reservation
from .forms import ReservationForm, SpaceFilterForm
import logging
from django.http import JsonResponse
from django.utils import timezone
import datetime

import datetime
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

def list_spaces(request):
    form = SpaceFilterForm(request.GET or None)
    spaces = Space.objects.all()
    if form.is_valid():
        office_type = form.cleaned_data.get('office_type')
        if (office_type):
            spaces = spaces.filter(office_type=office_type)
    return render(request, 'list_spaces.html', {'spaces': spaces, 'form': form})

@login_required
def make_reservation(request, space_id):
    space = get_object_or_404(Space, id=space_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.space = space
            reservation.user = request.user
            try:
                reservation.save()
                return redirect('list_reservations')
            except ValueError as e:
                form.add_error(None, str(e))
    else:
        form = ReservationForm()
    return render(request, 'make_reservation.html', {'form': form, 'space': space})

@login_required
def list_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'list_reservations.html', {'reservations': reservations})

def get_time_slots(request, space_id):
    date = request.GET.get('date')
    space = Space.objects.get(id=space_id)
    start_of_day = datetime.datetime.strptime(date, '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc)
    end_of_day = start_of_day + datetime.timedelta(days=1)
    
    reservations = Reservation.objects.filter(space=space, start_time__gte=start_of_day, end_time__lt=end_of_day)
    reserved_hours = set()
    
    for reservation in reservations:
        start_hour = reservation.start_time.hour
        end_hour = reservation.end_time.hour
        for hour in range(start_hour, end_hour):
            reserved_hours.add(hour)
    
    time_slots = {}
    for hour in range(7, 19):  # Assuming the office hours are from 7:00 to 18:00
        if hour in reserved_hours:
            time_slots[f'{hour}:00'] = 'unavailable'
        else:
            time_slots[f'{hour}:00'] = 'available'
    
    return JsonResponse(time_slots)