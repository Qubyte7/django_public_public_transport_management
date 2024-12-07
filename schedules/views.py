from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Schedule, Booking
from users.models import UserProfile
from .forms import BookingForm
from django.http import HttpResponse
from schedules.forms import SearchForm

@login_required
def book_ticket(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            num_seats = form.cleaned_data['num_seats']
            total_price = schedule.price_per_seat * num_seats

            if num_seats <= schedule.available_seats and user_profile.balance >= total_price:
                booking = Booking.objects.create(
                    user=request.user,
                    schedule=schedule,
                    num_seats=num_seats,
                    total_price=total_price
                )
                schedule.available_seats -= num_seats
                schedule.save()
                user_profile.balance -= total_price
                user_profile.save()
                return redirect('booking_confirmation', booking_id=booking.id)
            else:
                form.add_error(None, "Not enough seats available or insufficient balance.")
    else:
        form = BookingForm()

    context = {
        'schedule': schedule,
        'form': form,
        'user_balance': user_profile.balance,
    }
    return render(request, 'schedules/book_ticket.html', context)

@login_required
def booking_confirmation(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    return render(request, 'schedules/booking_confirmation.html', {'booking': booking})

@login_required
def show_booked_ticket(request):
    booked=Booking.objects.all()
    return render(request, 'schedules/booked_ticket.html',{'booked_ticket':booked})   
 
@login_required

def delete_booked_ticket(request, ticket_id):
    # Get the booking amount
    booked_ticket=Booking.objects.get(id=ticket_id)
    amount=booked_ticket.total_price
    # update the available seat
    schedule=Schedule.objects.get(id=booked_ticket.schedule.id);
    schedule.available_seats=schedule.available_seats+1;
    schedule.save()
    # Delete the booking
    booked_ticket.delete()
    # update the user booking
    user= UserProfile.objects.get(user=request.user)
    user.balance=amount;
    user.save()
    return redirect('/')