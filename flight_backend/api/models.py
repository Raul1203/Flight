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
    aircraft = models.CharField(max_length=50)
    gate = models.CharField(max_length=10, blank=True, null=True)
    terminal = models.CharField(max_length=10, blank=True, null=True)

    live_latitude = models.FloatField(blank=True, null=True)
    live_longitude = models.FloatField(blank=True, null=True)
    live_updated = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.flight_number} - {self.origin} to {self.destination}"


class DayWithMostFlights(models.Model):
    month = models.DateField()
    day = models.DateField()
    flight_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class MostVisitedDestination(models.Model):
    month = models.DateField()
    destination = models.CharField(max_length=255)
    visit_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class AircraftWithMostFlights(models.Model):
    month = models.DateField()
    aircraft = models.CharField(max_length=255)
    flight_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
