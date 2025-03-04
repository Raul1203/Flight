import requests
from celery import shared_task
from django.utils.dateparse import parse_datetime
from decouple import config
from .models import Flight

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
    return "Flight data updated successfully"
