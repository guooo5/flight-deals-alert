import os 
from dotenv import load_dotenv
import requests
load_dotenv()

SERPAPI_ENDPOINT = "https://serpapi.com/search"

class FlightSearch:
    #This class for talking to the Flight Search API
    
    def __init__(self):
        self._api_key = os.environ["SERPAPI_API_KEY"]
    
    def check_flights(self, origin_city_code, dest_city_code, from_time, to_time):
        params = {
            "engine": "google_flights",
            "departure_id": origin_city_code,
            "arrival_id": dest_city_code,
            "outbound_date": from_time,
            "return_date": to_time,
            "type": "1",
            "adults":"1",
            "currency": "USD",
            "api_key": self._api_key
        }
        
        response = requests.get(url=SERPAPI_ENDPOINT, params=params)
        
        if response.status_code != 200:
            print(f"check_flight() response code: {response.status_code}")
            return None 
        
        data = response.json()
        if "error" in data:
            print(f"API error: {data['error']}")
            return None 
        return data 