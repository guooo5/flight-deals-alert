class FlightData:
    #This class is for structuring the flight data
    def __init__(self, price, origin_airport, dest_airport, out_date, return_date):
        self.price = price
        self.origin_airport = origin_airport
        self.dest_airport = dest_airport
        self.out_date = out_date
        self.return_date = return_date

def find_cheapest_flight(data, return_date):
    if not data or (not data.get("best_flights") and not data.get("other_flights")): 
        print("No flight data")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A")
    
    #combine flights into one list
    all_flights = data.get("best_flights", []) + data.get("other_flights",[])
    
    #data from first flight in the list 
    first_flight = all_flights[0]
    lowest_price = first_flight["price"]
    origin = first_flight["flights"][0]["departure_airport"]["id"]
    destination = first_flight["flights"][-1]["arrival_airport"]["id"]
    out_date = first_flight["flights"][0]["departure_airport"]["time"].split(" ")[0]
    
    #initalize FlightData with first flight 
    cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)
    
    for flight in all_flights:
        #exception handling - has data but missing price, just skip
        try:
            price = flight["price"]
        except KeyError:
            print("No price available for this flight")
            continue 
        if price < lowest_price:
            lowest_price = price
            origin = flight["flights"][0]["departure_airport"]["id"]
            destination = flight["flights"][-1]["arrival_airport"]["id"]
            out_date = flight["flights"][0]["departure_airport"]["time"].split(" ")[0]
            cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)
            print(f"Lowest price to {destination} is USD {lowest_price}")
    return cheapest_flight
    
    
    