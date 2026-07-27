from pprint import pprint 

from data_manager import DataManager
data = DataManager()
sheet_data = data.get_data()

pprint(sheet_data)
