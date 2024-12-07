from django.urls import path
from . import views
from ..users.views import update_location
urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:schedule_id>/', views.book_ticket, name='book_ticket'),
    path('booking_confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('update_location/', update_location, name='update_location'),
]