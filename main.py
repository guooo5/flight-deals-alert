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
pprint(sheet_data)


#----set the dates 
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))


#-----do flight search 
flight_search = FlightSearch()

flights = flight_search.check_flights(
    origin_city_code='LHR',
    dest_city_code='CDG',
    from_time=tomorrow,
    to_time=six_month_from_today
)

# pprint(flights)


#-----show cheapest flight
cheapest_flight = find_cheapest_flight(flights, return_date=six_month_from_today.strftime("%Y-%m-%d"))

pprint(f"{sheet_data[0]['city']}: USD {cheapest_flight.price}")

if cheapest_flight.price != "N/A" and cheapest_flight.price < sheet_data[0]["lowestPrice"]:
    pprint(f"Lower price flight found to {sheet_data[0]['city']}!")
    data.update_lowest_price(sheet_data[0]["id"], cheapest_flight.price)