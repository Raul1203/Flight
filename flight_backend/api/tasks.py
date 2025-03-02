import requests
from celery import shared_task
from django.utils.dateparse import parse_datetime
from decouple import config
from .models import Flight

@shared_task
def fetch_and_store_flight_data():
    API_KEY = config('AVIATIONSTACK_API_KEY')
    
    url = "http://api.aviationstack.com/v1/flights"
    params = {
        "access_key": API_KEY,
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print("Error fetching flight data:", e)
        return "Error fetching flight data"
    
    # Process each flight in the response
    for flight_info in data.get("data", []):
        # Ensure the record is a dict before processing
        if not isinstance(flight_info, dict):
            print("Skipping record that is not a dict:", flight_info)
            continue

        # Extract basic flight data
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

        if not flight_number or not airline or not origin or not destination:
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
    return "Flight data updated successfully"
