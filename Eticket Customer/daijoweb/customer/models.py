from django.db import models

# Create your models here.
# customer/models.py
from django.db import models

# model tiket di database  
class Ticket(models.Model):
    name = models.TextField()
    email = models.TextField()
    phone = models.TextField()
    seating_plan = models.TextField()
    seat_number = models.TextField()
    check_in = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} - {self.seating_plan} - Seat {self.seat_number}'
