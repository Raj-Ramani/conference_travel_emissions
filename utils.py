from cities import City, CityCollection
from pathlib import Path
import csv

def read_attendees_file(filepath: Path) -> CityCollection:
    list_of_cities = []

    with open(filepath, newline="") as f:
        file_reader = csv.DictReader(f)
        for row in file_reader:     #using column name
            list_of_cities.append(City(row["city"], row["country"], int(row["N"]), float(row["lat"]), float(row["lon"])))
    
    
    return CityCollection(list_of_cities)
