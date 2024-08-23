#-# Json funcs, to read and write json files
import json
def write_json(file:str, json_dict:dict) -> None:
    with open(file, 'w') as f:
        f.write(json.dumps(json_dict, indent=4, sort_keys=True))

def read_json(file:str) -> dict:
    with open(file, 'r') as f:
        return json.load(f)
    

#-# Function to convert RGB values ​​to HEX values
def rgb_to_hex(red,green, blue):
    rgb = (red, green, blue)
    return '#%02x%02x%02x' % rgb


#-# Function that returns a string formatted with today's date
from datetime import date
def get_today():
    day_today = date.today().day
    month_today = date.today().month
    
    day   = day_today   if day_today   >= 10 else f"0{ day_today }"
    month = month_today if month_today >= 10 else f"0{month_today}"
    year  = date.today().year
    
    return f"{day}/{month}/{year}"