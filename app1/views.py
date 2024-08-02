# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Space, Reservation, UserProfile
from .forms import ReservationForm, SpaceFilterForm, EditProfileForm, UserProfileForm, CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash

import logging
from django.http import JsonResponse
from django.utils import timezone
import datetime

logger = logging.getLogger(__name__)

def home(request):
    office_types = ['single', 'multiple', 'meeting', 'lab', 'suite']
    featured_spaces = []

    for office_type in office_types:
        space = Space.objects.filter(office_type=office_type).first()
        if space:
            featured_spaces.append(space)

    return render(request, 'home.html', {'featured_spaces': featured_spaces})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('list_spaces')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('/')

def about(request):
    return render(request, 'about.html')

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

    return render(request, 'register.html', {'form': form})

def list_spaces(request):
    form = SpaceFilterForm(request.GET or None)
    spaces = Space.objects.all()
    if form.is_valid():
        office_type = form.cleaned_data.get('office_type')
        capacity = form.cleaned_data.get('capacity')
        location = form.cleaned_data.get('location')
        price_per_hour = form.cleaned_data.get('price_per_hour')
        
        if office_type:
            spaces = spaces.filter(office_type=office_type)
        if capacity:
            spaces = spaces.filter(capacity__gte=capacity)
        if location:
            spaces = spaces.filter(location__icontains=location)
        if price_per_hour:
            spaces = spaces.filter(price_per_hour__lte=price_per_hour)

    return render(request, 'list_spaces.html', {'spaces': spaces, 'form': form})

@login_required
def make_reservation(request, space_id):
    space = get_object_or_404(Space, id=space_id)
    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        try:
            reservation = Reservation(
                space=space,
                user=request.user,
                start_time=start_time,
                end_time=end_time,
                status='pending'
            )
            reservation.save()
            return redirect('list_reservations')
        except ValueError as e:
            form = ReservationForm()
            return render(request, 'make_reservation.html', {
                'form': form, 
                'space': space,
                'error': str(e)
            })
    else:
        form = ReservationForm()
    return render(request, 'make_reservation.html', {'form': form, 'space': space})




@login_required
def list_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'list_reservations.html', {'reservations': reservations})

@login_required
def confirm_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user, status='pending')
    reservation.status = 'confirmed'
    reservation.save()
    return redirect('list_reservations')

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user, status='pending')
    reservation.delete()
    return redirect('list_reservations')


@login_required
def get_time_slots(request, space_id):
    date_str = request.GET.get('date')
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    space = get_object_or_404(Space, id=space_id)

    # Define the start and end of the day
    start_of_day = datetime.datetime.combine(date, datetime.time.min)
    end_of_day = datetime.datetime.combine(date, datetime.time.max)

    reservations = Reservation.objects.filter(space=space, start_time__range=(start_of_day, end_of_day))

    # Define your time slots here (e.g., every hour from 9am to 5pm)
    time_slots = []
    current_time = start_of_day.replace(hour=9)
    end_time = start_of_day.replace(hour=17)
    
    while current_time < end_time:
        slot_end_time = current_time + datetime.timedelta(hours=1)
        overlapping_reservations = reservations.filter(
            start_time__lt=slot_end_time,
            end_time__gt=current_time
        )

        if overlapping_reservations.exists():
            if overlapping_reservations.filter(status='pending').exists():
                status = 'pending'
            else:
                status = 'unavailable'
        else:
            status = 'available'
        
        time_slots.append({
            'start_time': current_time.strftime('%H:%M'),
            'end_time': slot_end_time.strftime('%H:%M'),
            'status': status
        })

        current_time = slot_end_time

    return JsonResponse({'time_slots': time_slots})


@login_required
def reservation_detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    return render(request, 'reservation_detail.html', {'reservation': reservation})


@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = EditProfileForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)
    
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    
    return render(request, 'change_password.html', {'form': form})