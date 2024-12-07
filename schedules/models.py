from django.db import models
from django.contrib.auth.models import User

class District(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class TransportCompany(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Route(models.Model):
    source = models.ForeignKey(District, on_delete=models.CASCADE, related_name='source_routes')
    destination = models.ForeignKey(District, on_delete=models.CASCADE, related_name='destination_routes')
    def __str__(self):
        return f"{self.source} - {self.destination}"

class  Schedule(models.Model):
    company = models.ForeignKey(TransportCompany, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    vehicle_plate = models.CharField(max_length=20)
    departure_time = models.DateTimeField()
    estimated_journey_time = models.DurationField()
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    price_per_seat = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.company} - {self.route} - {self.departure_time}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    num_seats= models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.schedule} - {self.num_seats} seats"