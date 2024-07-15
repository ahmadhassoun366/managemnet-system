from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Space(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    amenities = models.TextField()
    location = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Reservation(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    cost = models.DecimalField(max_digits=6, decimal_places=2)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username