# models.py
from django.db import models
from django.contrib.auth.models import User

# models.py
from django.db import models
from django.contrib.auth.models import User

class Space(models.Model):
    OFFICE_TYPES = [
        ('single', 'Single Office for 1 Person'),
        ('multiple', 'Office for Multiple Persons'),
        ('meeting', 'Meeting Room'),
        ('lab', 'Lab with PCs'),
        ('suite', 'Private Office Suite'),
     
    ]
    
    name = models.CharField(max_length=100)
    office_type = models.CharField(max_length=15, choices=OFFICE_TYPES, default='single')
    capacity = models.IntegerField()
    amenities = models.TextField()
    location = models.TextField()
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='space_images/', blank=True, null=True)  # Add this line

    def __str__(self):
        return self.name


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ]

    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        if self.start_time >= self.end_time:
            raise ValueError("End time must be after start time.")
        
        overlapping_reservations = Reservation.objects.filter(
            space=self.space,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(id=self.id).exclude(status='cancelled')
        
        if overlapping_reservations.exists():
            raise ValueError("This space is already reserved for the selected time.")
        
        super().save(*args, **kwargs)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.jpg')

    def __str__(self):
        return self.user.username