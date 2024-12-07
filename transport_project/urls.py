from django.contrib import admin
from django.urls import path
from users import views as user_views
from schedules import views as schedule_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home, name='home'),
    path('accounts/register/', user_views.register, name='register'),
    path('accounts/login/', user_views.login_view, name='login'),
    path('accounts/logout/', user_views.logout_view, name='logout'),
    path('update_location/', user_views.update_location, name='update_location'),
    path('book/<int:schedule_id>/', schedule_views.book_ticket, name='book_ticket'),
    path('booking_confirmation/<int:booking_id>/', schedule_views.booking_confirmation, name='booking_confirmation'),
    path('delete_booked_ticket/<int:ticket_id>/', schedule_views.delete_booked_ticket,name='Delete booked ticket')
]