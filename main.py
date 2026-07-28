import requests_cache #save API responses locally 
from pprint import pprint 
from datetime import datetime, timedelta

from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight

#------conserve requests 
requests_cache.install_cache(
    "flight_cache",
    url_expire_after={
        #cache everything (except sheety) for 1hour 
        "*.sheety.co*": requests_cache.DO_NOT_CACHE,
        "*":3600,
    }
)

#----talking to sheety 
data = DataManager()
sheet_data = data.get_data()
# pprint(sheet_data)


#----set the dates 
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))


#----- search for cheapest flights for all destinations 
ORIGIN_CITY_IATA = "JFK"

flight_search = FlightSearch()

for dest in sheet_data:
    pprint(f"Getting flights for {dest['city']}...")
    flights = flight_search.check_flights(
        origin_city_code=ORIGIN_CITY_IATA,
        dest_city_code=dest['iataCode'],
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    cheapest_flight = find_cheapest_flight(flights, return_date=six_month_from_today.strftime("%Y-%m-%d"))
    pprint(f"{dest['city']}: USD {cheapest_flight.price}")
    
    if cheapest_flight.price != "N/A" and cheapest_flight.price < dest["lowestPrice"]:
        pprint(f"Lower price flight found to {dest['city']}!")
        data.update_lowest_price(dest["id"], cheapest_flight.price)