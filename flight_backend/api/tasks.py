import requests
from celery import shared_task
from django.utils.dateparse import parse_datetime
from decouple import config
from django.db.models import Count, Max
from django.db.models.functions import TruncDay
from django.utils.timezone import now
from .models import (
    Flight,
    MostVisitedDestination,
    AircraftWithMostFlights,
    DayWithMostFlights,
    AirplaneLocation,
    AirportWithMostDepartures
)

@shared_task
def as_flight_data():
    PRIMARY_API_KEY = config('AVIATIONSTACK_API_KEY')
    ALT_API_KEY = config('AVIATIONSTACK_API_KEY_2')  
    url = "http://api.aviationstack.com/v1/flights"
    
    def get_data(api_key):
        params = {"access_key": api_key}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    try:
        data = get_data(PRIMARY_API_KEY)
        if "error" in data:
            error_message = data["error"].get("message", "").lower()
            if "quota" in error_message or "limit" in error_message:
                print("Primary API key exhausted, switching to alternate key")
                data = get_data(ALT_API_KEY)
    except requests.RequestException as e:
        print("Error fetching flight data:", e)
        return "Error fetching flight data"

    for flight_info in data.get("data", []):
        if not isinstance(flight_info, dict):
            print("Skipping record that is not a dict:", flight_info)
            continue

        flight_date = flight_info.get("flight_date")
        flight_status = flight_info.get("flight_status", "scheduled")
        
        flight_data = flight_info.get("flight") or {}
        airline_data = flight_info.get("airline") or {}
        departure = flight_info.get("departure") or {}
        arrival = flight_info.get("arrival") or {}
        aircraft_data = flight_info.get("aircraft") or {}
        live = flight_info.get("live") or {}

        flight_number = flight_data.get("iata")
        airline = airline_data.get("name", "")
        origin = departure.get("airport", "")
        destination = arrival.get("airport", "")

        if not flight_number or not airline or not origin or not destination or not aircraft_data:
            print("Skipping record due to missing required fields:", flight_info)
            continue

        departure_time = parse_datetime(departure.get("scheduled")) if departure.get("scheduled") else None
        arrival_time = parse_datetime(arrival.get("scheduled")) if arrival.get("scheduled") else None

        status = flight_status
        
        aircraft = aircraft_data.get("iata", "")
        gate = departure.get("gate", "")
        terminal = departure.get("terminal", "")

        live_latitude = live.get("latitude")
        live_longitude = live.get("longitude")
        live_updated = parse_datetime(live.get("updated")) if live.get("updated") else None

        if flight_number:
            Flight.objects.update_or_create(
                flight_number=flight_number,
                defaults={
                    "airline": airline,
                    "origin": origin,
                    "destination": destination,
                    "departure_time": departure_time,
                    "arrival_time": arrival_time,
                    "status": status,
                    "aircraft": aircraft,
                    "gate": gate,
                    "terminal": terminal,
                    "live_latitude": live_latitude,
                    "live_longitude": live_longitude,
                    "live_updated": live_updated,
                }
            )
    update_flight_statistics.delay()        
    return "Flight data updated successfully"

@shared_task
def update_flight_statistics():
    current_date = now().date()
    current_month = current_date.replace(day=1)
    
    # --- Top 3 Destinations with Most Landings ---
    destinations = (
        Flight.objects.filter(departure_time__year=current_date.year, departure_time__month=current_date.month)
        .values('destination')
        .annotate(visit_count=Count('id'), latest_landing=Max('departure_time'))
        .order_by('-visit_count', '-latest_landing')[:3]
    )
    for rank, dest in enumerate(destinations, start=1):
        record = MostVisitedDestination.objects.filter(month=current_month, rank=rank).first()
        if record:
            if dest['visit_count'] > record.visit_count or (
                dest['visit_count'] == record.visit_count and dest['latest_landing'] > record.latest_landing
            ):
                record.destination = dest['destination']
                record.visit_count = dest['visit_count']
                record.latest_landing = dest['latest_landing']
                record.save()
        else:
            MostVisitedDestination.objects.create(
                month=current_month,
                destination=dest['destination'],
                visit_count=dest['visit_count'],
                latest_landing=dest['latest_landing'],
                rank=rank
            )
    
    # --- Top 3 Aircraft with Most Flights ---
    aircrafts = (
        Flight.objects.filter(departure_time__year=current_date.year, departure_time__month=current_date.month)
        .values('aircraft', 'airline')
        .annotate(flight_count=Count('id'))
        .order_by('-flight_count')[:3]
    )

    for rank, ac in enumerate(aircrafts, start=1):
        record = AircraftWithMostFlights.objects.filter(month=current_month, rank=rank).first()
        if record:
            if ac['flight_count'] > record.flight_count:
                record.aircraft = ac['aircraft']
                record.airline = ac['airline']
                record.flight_count = ac['flight_count']
                record.save()
        else:
            AircraftWithMostFlights.objects.create(
                month=current_month,
                aircraft=ac['aircraft'],
                airline=ac['airline'],
                flight_count=ac['flight_count'],
                rank=rank
            )
    
    # --- Day with Most Flights and Flight Positions ---
    day_stats = (
    Flight.objects.filter(departure_time__year=current_date.year, departure_time__month=current_date.month)
    .annotate(day=TruncDay('departure_time'))
    .values('day')
    .annotate(flight_count=Count('id'))
    .order_by('-flight_count')
    )

    if day_stats.exists():  
        top_day_data = day_stats[0]
        record = DayWithMostFlights.objects.filter(month=current_month).first()

        if record:
            if top_day_data['flight_count'] >= record.flight_count:  # Ensure updates if same count
                record.day = top_day_data['day']
                record.flight_count = top_day_data['flight_count']
                record.save()

                record.locations.all().delete()  

                flights_on_top_day = Flight.objects.filter(departure_time__date=top_day_data['day'])
                for flight in flights_on_top_day:
                    lat = flight.live_latitude
                    lon = flight.live_longitude
                    dest = None
                    if lat is None and flight.status.lower() == 'landed':
                        dest = flight.destination  

                    AirplaneLocation.objects.create(
                        day_statistic=record,
                        latitude=lat,
                        longitude=lon,
                        status=flight.status,
                        airline=flight.airline,
                        aircraft=flight.aircraft,
                        destination=dest,
                    )
        else:
            record = DayWithMostFlights.objects.create(
                month=current_month,
                day=top_day_data['day'],
                flight_count=top_day_data['flight_count']
            )

            flights_on_top_day = Flight.objects.filter(departure_time__date=top_day_data['day'])
            for flight in flights_on_top_day:
                lat = flight.live_latitude
                lon = flight.live_longitude
                dest = None
                if lat is None and flight.status.lower() == 'landed':
                    dest = flight.destination

                AirplaneLocation.objects.create(
                    day_statistic=record,
                    latitude=lat,
                    longitude=lon,
                    status=flight.status,
                    airline=flight.airline,
                    aircraft=flight.aircraft,
                    destination=dest,
                )

# --- Airport with most departures ---
    airport_stats = (
        Flight.objects.filter(departure_time__year=current_date.year, departure_time__month=current_date.month)
        .values('origin')
        .annotate(departure_count=Count('id'))
        .order_by('-departure_count')
    )

    if airport_stats:
        top_airport_data = airport_stats[0]
        airport_code = top_airport_data['origin']
        departure_count = top_airport_data['departure_count']

        airline_stats = (
            Flight.objects.filter(
                departure_time__year=current_date.year,
                departure_time__month=current_date.month,
                origin=airport_code
            )
            .values('airline')
            .annotate(airline_count=Count('id'))
            .order_by('-airline_count')
        )

        airline_counts = {entry['airline']: entry['airline_count'] for entry in airline_stats}
        AirportWithMostDepartures.objects.update_or_create(
            month=current_month,
            defaults={
                'airport': airport_code,
                'departure_count': departure_count,
                'airline_departure_counts': airline_counts
            }
        )