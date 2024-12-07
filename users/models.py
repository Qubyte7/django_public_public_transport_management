from django.db import models
from django.contrib.auth.models import User

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     location = models.CharField(max_length=100, blank=True, null=True)

#     def __str__(self):
#         return self.user.username
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.user.username