import requests_cache #save API responses locally 
from pprint import pprint 
from datetime import datetime, timedelta

from data_manager import DataManager
from flight_search import FlightSearch

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

pprint(flights)