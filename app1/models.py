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
        # ('coworking', 'Co-working Space'),
        # ('hotdesk', 'Hot Desk Area'),
        # ('conference', 'Conference Room'),
        # ('studio', 'Creative Studio'),
        # ('training', 'Training Room'),
    ]
    
    name = models.CharField(max_length=100)
    office_type = models.CharField(max_length=15, choices=OFFICE_TYPES, default='single')
    capacity = models.IntegerField()
    amenities = models.TextField()
    location = models.TextField()
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.start_time >= self.end_time:
            raise ValueError("End time must be after start time.")
        
        overlapping_reservations = Reservation.objects.filter(
            space=self.space,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        )
        if overlapping_reservations.exists():
            raise ValueError("This space is already reserved for the selected time.")
        
        super().save(*args, **kwargs)
