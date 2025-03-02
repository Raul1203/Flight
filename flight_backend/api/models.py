from django.db import models

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    airline = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("scheduled", "Scheduled"),
            ("active", "Active"), 
            ("landed", "Landed"),
            ("cancelled", "Cancelled"),
            ("delayed", "Delayed"),
        ],
        default="scheduled",
    )
    aircraft = models.CharField(max_length=50, blank=True, null=True)
    gate = models.CharField(max_length=10, blank=True, null=True)
    terminal = models.CharField(max_length=10, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.flight_number} - {self.origin} to {self.destination}"
