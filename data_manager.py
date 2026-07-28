#This class is for talking to the Google Sheet
import requests
import os 
from requests.auth import HTTPBasicAuth #sheety uses this for basic auth
from dotenv import load_dotenv

load_dotenv()

SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/175d38ae177d32cdc9cd7dcc2c385901/flightDeals/prices"

class DataManager:
    
    def __init__(self):
        self._user = os.environ["SHEETY_USER"]
        self._password = os.environ["SHEETY_PASSWORD"]
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.dest_data = {}
    
    #use sheety api to get all data in sheet 
    def get_data(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, auth=self._authorization)
        data = response.json()
        self.dest_data = data["prices"]
        return self.dest_data
    
    
    #---updated price in the spreadsheet
    def update_lowest_price(self, row_id, new_price):
        new_data = {
            "price": {
                "lowestPrice": new_price
            }
        }
        requests.put(
            url=f"{SHEETY_PRICES_ENDPOINT}/{row_id}",
            json=new_data,
            auth=self._authorization
        )
        