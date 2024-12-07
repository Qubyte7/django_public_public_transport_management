 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserLoginForm
from schedules.forms import  SearchForm
from .models import UserProfile
from schedules.models import Schedule
from django.db.models import Q
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from datetime import timedelta
from schedules.models import Booking
import json
from collections import defaultdict

from django.core.serializers.json import DjangoJSONEncoder

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            balance=form.cleaned_data.get('balance')
            user = User.objects.create(username=username, email=email, password=make_password(password))
            UserProfile.objects.create(user=user,balance=balance)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def get_district_from_coordinates(latitude, longitude):
    try:
        # Initialize the geocoder with a user agent (required by Nominatim)
        geolocator = Nominatim(user_agent="geoapiExercises")
        
        # Create the location string with latitude and longitude
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        
        # Fetch the address components from the location
        if location:
            address = location.raw['address']
            # You can adjust the hierarchy of the returned address based on how districts are named in your region
            district = address.get('city_district') or address.get('county') or address.get('state_district')
            return district if district else "District not found"
        else:
            return "Location not found"
    except GeocoderTimedOut:
        return "Error: Geocoder timed out"
    except Exception as e:
        return f"Error: {e}"
    
@login_required
def update_location(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        print(longitude)
        print(latitude)
        district = get_district_from_coordinates(latitude, longitude)  # Get the district from coordinates
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.latitude = latitude
        user_profile.longitude = longitude
        user_profile.district = district  # Save the district in the user profile

        user_profile.save()
        return redirect('home')
    return redirect('home')


@login_required
def home(request):
    user_profile = UserProfile.objects.get(user=request.user)
    district = get_district_from_coordinates(user_profile.latitude or "", user_profile.longitude or "")
    print(district)
    schedules = None
    search_form = SearchForm()
    booked = Booking.objects.filter(user=request.user)
    bookedStatistics = defaultdict(int)

    # Group bookings by the day and count them
    for booking in booked:
        day_
        label = booking.created_at.strftime('%Y-%m-%d')  
        bookedStatistics[day_label] += 1

    # Prepare data for Chart.js
    labels = list(bookedStatistics.keys())
    booked_counts = list(bookedStatistics.values())

    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            schedules = Schedule.objects.filter(
                Q(company__name__icontains=query) |
                Q(route__source__name__icontains=query) |
                Q(route__destination__name__icontains=query)
            )
    else:
        if district == "District not found" or district == "Location not found" or district == "Error: HTTP Error 403: Forbidden":
            schedules = Schedule.objects.all()
            district = "Allow location to continue"
        else:
            schedules = Schedule.objects.filter(Q(route__source__name=district) | Q(route__destination__name=district))
    
    context = {
        'schedules': schedules,
        'booked_ticket': booked,
        'district': district,
        'search_form': search_form,
        'booked_statistics': json.dumps({
            'labels': labels,
            'booked_counts': booked_counts
        }),
    }

    return render(request, 'users/home.html', context)
